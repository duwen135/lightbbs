# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'lb_follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'), primary_key=True)
    is_follow = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
