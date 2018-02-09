# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Favorite(db.Model):
    __tablename__ = 'lb_favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('lb_topics.id'), primary_key=True)
    is_favorite = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow())