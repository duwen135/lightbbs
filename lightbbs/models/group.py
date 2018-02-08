# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Group(db.Model):
    __tablename__ = 'lb_groups'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    group_type = db.Column(db.Integer)
    group_name = db.Column(db.String(64), unique=True)
    user_num = db.Column(db.Integer)
