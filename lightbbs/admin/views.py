# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, request, redirect, url_for, flash, current_app, abort
from . import admin
from flask_login import current_user, login_required
from ..decorators import admin_required, permission_required
from datetime import datetime
from ..import db
from .forms import UserEdit, NodeForm, TopicForm
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

@admin.route('/user_delete/<int:id>', methods=['POST'])
@admin_required
@login_required
def user_delete(id):
    user = User.query.first_or_404(id)
    db.session.delete(user)
    flash('删除成功！')
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

@admin.route('/node_delete/<int:id>', methods=['POST'])
@admin_required
@login_required
def node_delete(id):
    node = Node.query.get_or_404(id)
    db.session.delete(node)
    flash('节点删除成功!')
    return render_template('admin/node_list.html', node=node)


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

@admin.route('/topic_delete/<int:id>', methods=['POST'])
@admin_required
@login_required
def topic_delete(id):
    topic = Topic.query.get_or_404(id)
    db.session.delete(topic)
    flash('删除成功!')
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_top/<int:id>', methods=['POST'])
@admin_required
@login_required
def top(id):
    topic = Topic.query.get_or_404(id)
    topic.is_top = True
    db.session.add(topic)
    flash('置顶成功！')
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_untop/<int:id>', methods=['POST'])
@admin_required
@login_required
def untop(id):
    topic = Topic.query.get_or_404(id)
    topic.is_top = False
    db.session.add(topic)
    flash('取消置顶！')
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_hidden/<int:id>', methods=['POST'])
@admin_required
@login_required
def hidden(id):
    topic = Topic.query.get_or_404(id)
    topic.is_hidden = True
    db.session.add(topic)
    flash('已设置隐藏！')
    return render_template('/admin/topics.html', topic=topic)

@admin.route('/topic_unhidden/<int:id>', methods=['POST'])
@admin_required
@login_required
def unhidden(id):
    topic = Topic.query.get_or_404(id)
    topic.is_hidden = False
    db.session.add(topic)
    flash('已设置显示！')
    return render_template('/admin/topics.html', topic=topic)


#友情链接

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
    return render_template('/admin/topics.html', pages=pages)
