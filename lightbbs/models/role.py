# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Role(db.Model):
    __tablename__ = 'lb_roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    defoult = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user_num = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


