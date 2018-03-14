# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, request, redirect, url_for, flash, current_app, abort
from . import admin
from flask_login import current_user, login_required
from ..decorators import admin_required, permission_required
from ..import db
from ..models.user import User


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
    user = User.query.filter_by(id=id).first_or_404()