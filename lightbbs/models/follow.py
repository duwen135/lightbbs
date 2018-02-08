# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from . import user


class Follow(db.Model):
    __tablename__ = 'lb_follows'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'), primary_key=True)
    add_time = db.Column(db.DateTime)
