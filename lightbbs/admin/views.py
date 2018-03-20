# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, request, redirect, url_for, flash, current_app, abort
from . import admin
from flask_login import current_user, login_required
from ..decorators import admin_required, permission_required
from datetime import datetime
from ..import db
from .forms import UserEdit, NodeForm, TopicForm, PageForm, LinkForm
from ..models.user import User
from ..models.role import Role
from ..models.node import Node
from ..models.topic import Topic
from ..models.link import Link
from ..models.page import Page


#用户管理
@admin.route('/users')
@admin_required
@login_required
def user_list():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.regtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('/admin/users.html', users=users)

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def user_edit(id):
    user = User.query.get_or_404(id)
    form = UserEdit(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.homepage = form.homepage.data
        user.location = form.location.data
        user.signature = form.signature.data
        user.about_me = form.about_me.data
        user.integral = form.integral.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        db.session.add(user)
        flash('用户资料已经更新。')
        return redirect(url_for('.user', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.homepage.data = user.homepage
    form.location.data = user.location
    form.signature.data = user.signature
    form.about_me.data = user.about_me
    form.integral.data = user.integral
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    return render_template('/admin/user_edit.html', form=form, user=user)

@admin.route('/user_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def user_delete(id):
    user = User.query.first_or_404(id)
    if user:
        db.session.delete(user)
        flash('删除成功！')
        return redirect(url_for('admin.user_list'))
    render_template('/admin/users.html', user=user)

#节点管理
@admin.route('/nodes')
@admin_required
@login_required
def node_list():
    parent_nodes = Node.query.filter_by(parent_id=0).all()

    def get_node(parent_node):
        nodes = Node.query.filter_by(parent_id=parent_node.id).all()
        return nodes

    return render_template('admin/nodes.html', parent_nodes=parent_nodes, get_node=get_node)

@admin.route('/node_add', methods=['GET', 'POST'])
@admin_required
@login_required
def node_add():
    form = NodeForm()
    if form.validate_on_submit():
        node = Node(
            name=form.name.data,
            parent_id=form.parent_id.data,
            keywords=form.keywords.data,
            content=form.content.data,
            master_id=form.master_id.data
        )
        db.session.add(node)
        flash('节点创建成功！')
        return redirect(url_for('admin.node_list'))
    return render_template('admin/node_add.html', form=form)

@admin.route('/node_edit/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def node_edit(id):
    node = Node.query.get_or_404(id)
    form = NodeForm(node=node)
    if form.validate_on_submit():
        node.name = form.name.data,
        node.parent_id = form.parent_id.data,
        node.keywords = form.keywords.data,
        node.content = form.content.data,
        node.master_id = form.master_id.data

        db.session.add(node)
        flash('节点修改成功！')
        return redirect(url_for('admin.node_list'))
    return render_template('admin/node_edit.html', node=node, form=form)

@admin.route('/node_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def node_delete(id):
    node = Node.query.get_or_404(id)
    if node:
        db.session.delete(node)
        flash('节点删除成功!')
        return redirect(url_for('admin.node_list'))
    return render_template('admin/nodes.html', node=node)


#话题管理
@admin.route('/topic_list')
@admin_required
@login_required
def topic_list():
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.order_by(Topic.addtime.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    return render_template('/admin/topics.html', topics=topics)

@admin.route('/topic_add', methods=['GET', 'POST'])
@admin_required
@login_required
def topic_add():
    form = TopicForm()
    form.node.choices = [(n.id, n.name) for n in Node.query.order_by(Node.id).all()]
    if form.validate_on_submit():
        topic = Topic(node_id=form.node.data,
                      sender_id=current_user._get_current_object().id,
                      title=form.title.data,
                      content=form.content.data,
                      keywords=form.keywords.data,
                      addtime=datetime.utcnow())
        db.session.add(topic)
        flash('话题发布成功！')
        return redirect(url_for('admin.topics'))
    return render_template('/admin/topic_add.html', form=form)

@admin.route('/topic_edit/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def topic_edit(id):
    topic = Topic.query.get_or_404(id)
    form = TopicForm()
    form.node.choices = [(n.id, n.name) for n in Node.query.order_by(Node.id).all()]
    if form.validate_on_submit():
        topic.node_id = form.node.data
        topic.title = form.title.data
        topic.content = form.content.data
        topic.keywords = form.keywords.data
        topic.update_time = datetime.utcnow()
        db.session.add(topic)
        flash('这篇文章已经更新了。')
        return redirect(url_for('admin.topics', id=topic.id))
    form.node.data = topic.node_id
    form.title.data = topic.title
    form.content.data = topic.content
    form.keywords.data = topic.keywords
    return render_template('/admin/topic_edit.html', form=form)

@admin.route('/topic_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def topic_delete(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        db.session.delete(topic)
        flash('删除成功!')
        return redirect(url_for('admin.topic_list'))
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_top/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def top(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        topic.is_top = True
        db.session.add(topic)
        flash('置顶成功！')
        return redirect(url_for('admin.topic_list'))
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_untop/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def untop(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        topic.is_top = False
        db.session.add(topic)
        flash('取消置顶！')
        return redirect(url_for('admin.topic_list'))
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_hidden/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def hidden(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        topic.is_hidden = True
        db.session.add(topic)
        flash('已设置隐藏！')
        return redirect(url_for('admin.topic_list'))
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_unhidden/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def unhidden(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        topic.is_hidden = False
        db.session.add(topic)
        flash('已设置显示！')
        return redirect(url_for('admin.topic_list'))
    return render_template('/admin/topics.html', topic=topic)


#友情链接
@admin.route('/link_list')
@admin_required
@login_required
def link_list():
    page = request.args.get('page', 1, type=int)
    pagination = Link.query.order_by(Link.name).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'], error_out=False
    )
    links = pagination.items
    return render_template('/admin/links.html', links=links)

@admin.route('/link_add', methods=['GET', 'POST'])
@admin_required
@login_required
def link_add():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(
            name=form.name.data,
            url = form.url.data,
            logo = form.logo.data,
            is_hidden = form.is_hidden.data
        )
        db.session.add(link)
        flash('添加友情链接成功！')
        return redirect(url_for('admin.link_list'))
    return render_template('/admin/link_add.html', form=form)

@admin.route('/link_edit/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def link_edit(id):
    link = Link.query.get_or_404(id)
    form = LinkForm()
    if form.validate_on_submit():
        link.name = form.name.data,
        link.url = form.url.data,
        link.logo = form.logo.data,
        link.is_hidden = form.is_hidden.data
        db.session.add(link)
        flash('友情链接更新成功！')
        return redirect(url_for('admin.link_list'))
    form.name.data = link.name
    form.url.data = link.url
    form.logo.data = link.logo
    form.is_hidden.data = link.is_hidden
    return render_template('/admin/link_edit.html', link=link, form=form)

@admin.route('/link_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def link_delete(id):
    link = Link.query.get_or_404(id)
    if link:
        db.session.delete(link)
        flash('友情链接删除成功！')
        return redirect(url_for('admin.link_list'))
    return render_template('/admin/links.html', link=link)


#单页
@admin.route('/page_list')
@admin_required
@login_required
def page_list():
    page = request.args.get('page', 1, type=int)
    pagination = Page.query.order_by(Page.add_time.desc()).paginate(
        page, per_page=current_app.config['LIGHTBBS_POSTS_PER_PAGE'],
        error_out=False)
    pages = pagination.items
    return render_template('/admin/pages.html', pages=pages)

@admin.route('/page_add', methods=['GET', 'POST'])
@admin_required
@login_required
def page_add():
    form = PageForm()
    if form.validate_on_submit():
        page = Page(
            title = form.title.data,
            keywords = form.keywords.data,
            content = form.content.data,
            go_url = form.go_url.data,
            is_hidden = form.is_hidden.data
        )
        db.session.add(page)
        flash('单页添加成功！')
        return redirect(url_for('admin.page_list'))
    return render_template('/admin/page_add.html', form=form)

@admin.route('/page_edit/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def page_edit(id):
    page = Page.query.get_or_404(id)
    form = PageForm()
    if form.validate_on_submit():
        page.title = form.title.data,
        page.keywords = form.keywords.data,
        page.content = form.content.data,
        page.go_url = form.go_url.data,
        page.is_hidden = form.is_hidden.data

        db.session.add(page)
        flash('单页更新成功！')
        return redirect(url_for('admin.page_list'))
    form.title.data = page.title
    form.keywords.data = page.keywords
    form.content.data = page.content
    form.go_url.data = page.go_url
    form.is_hidden.data = page.is_hidden
    return render_template('/admin/page_edit.html', page=page, form=form)

@admin.route('/page_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def page_delete(id):
    page = Page.query.get_or_404(id)
    if page:
        db.session.delete(page)
        flash('单页删除成功！')
        return redirect(url_for('admin.page_list'))
    return render_template('/admin/pages.html', page=page)