# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, request, redirect, url_for, flash, current_app, abort
from . import admin
from flask_login import current_user, login_required
from ..decorators import admin_required, permission_required
from ..import db
from .forms import UserEdit
from ..models.user import User
from ..models.role import Role


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

@admin.route('/edit/<id>', methods=['GET', 'POST'])
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

@admin.route('/delete/<id>', methods=['POST'])
@admin_required
@login_required
def user_delete(id):
    user = User.query.first_or_404(id)
    db.session.delete(user)
    flash('删除成功！')
    render_template('/admin/users.html', user=user)