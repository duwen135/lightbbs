# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'lb_comments'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('lb_topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow())
