# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = 'lb_notifications'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('lb_topics.id'))
    comment_by = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    topic_sender_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    type = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow())
