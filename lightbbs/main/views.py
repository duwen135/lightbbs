# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, TopicForm, CommentForm
from .. import db
from ..decorators import admin_required, permission_required
from ..models.role import Role, Permission
from ..models.user import User
from ..models.comment import Comment
from ..models.topic import Topic
from ..models.node import Node
from ..models.tag import Tag

#首页部分
@main.route('/', methods=['GET', 'POST'])
def index():
    form = TopicForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        topic = Topic(content=form.content.data,
                      sender_id=current_user._get_current_object())
        db.session.add(topic)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_topics
    else:
        query = Topic.query
    pagination = query.order_by(Topic.addtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    return render_template('index.html', form=form, topics=topics,
                           show_followed=show_followed, pagination=pagination)

#首页话题列表响应
@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

#节点部分
@main.route('/nodes')
def node_list():
    parent_nodes = Node.query.order_by(Node.parent_id).all()
    nodes = Node.query.filter_by(parent_id = parent_nodes).all()
    return render_template('nodes.html', parent_nodes=parent_nodes, nodes=nodes)

@main.route('/nodes/<name>')
def node(name):
    node = Node.query.filter_by(name=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = node.topics.order_by(Topic.addtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    return render_template('node.html', node=node, topics=topics, pagination=pagination)

#用户部分
@main.route('/users')
def user_list():
    new_users = User.query.limit(30).order_by(User.regtime.desc()).all()
    hot_users = User.query.limit(30).order_by(User.follow_num.desc()).all()
    return render_template('users.html', new_users=new_users, hot_users=hot_users)


@main.route('/users/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.topics.order_by(Topic.addtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    pagination2 = user.comments.order_by(Comment.time.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    return render_template('user.html', user=user, topics=topics,
                           pagination=pagination, pagination2=pagination2)



@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的个人资料已经更新。')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('用户资料已经更新。')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

#tag部分
@main.route('/tags')
def tag_list():
    tags = Tag.query.limit(30).order_by(Tag.topic_num.desc()).all()
    return render_template('tags.html', tags=tags)

@main.route('/tags/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(tag_name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = tag.topics.order_by(Topic.addtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    return render_template('tag.html', tag=tag, topics=topics, pagination=pagination)

#话题部分

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    topic = Topic.query.get_or_404(id)
    if current_user != topic.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = TopicForm()
    if form.validate_on_submit():
        topic.content = form.content.data
        db.session.add(topic)
        flash('这篇文章已经更新了。')
        return redirect(url_for('.topic', id=topic.id))
    form.content.data = topic.content
    return render_template('edit_topic.html', form=form)

#评论部分
@main.route('/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    topic = Topic.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          topic=topic,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('你的评论已经发表了。')
        return redirect(url_for('.topic', id=topic.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (topic.comments.count() - 1) // \
               current_app.config['LIGHTBBS_COMMENTS_PER_PAGE'] + 1
    pagination = topic.comments.order_by(Comment.time.asc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('topic.html', topics=[topic], form=form,
                           comments=comments, pagination=pagination)



#关注部分
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('您已经在关注这个用户了。')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户。')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['LIGHTBBS_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['LIGHTBBS_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

#收藏部分
@main.route('/favorite/<username>')
def favorite(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户。')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.favorites.paginate(
        page, per_page=current_app.config['LIGHTBBS_FOLLOWERS_PER_PAGE'],error_out=False)
    topics = pagination.items
    return render_template('favorite.html', user=user, topics=topics, pagination=pagination)

#评论审核部分
@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.time.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

#小工具部分

#统计部分
#单页部分
#通知部分
#搜藏部分
#友情连接部分
#信息部分