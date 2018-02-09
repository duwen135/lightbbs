# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Topic(db.Model):
    __tablename__ = 'lb_topics'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('lb_nodes.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    title = db.Column(db.String(64))
    keywords = db.Column(db.String(64))
    content = db.Column(db.Text)
    addtime = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, default=datetime.utcnow())
    last_reply = db.Column(db.DateTime, default=datetime.utcnow())
    views = db.Column(db.Integer)
    comment_num = db.Column(db.Integer)
    favorite_num = db.Column(db.Integer)
    is_close_comment = db.Column(db.Boolean)
    is_top = db.Column(db.Boolean)
    is_hidden = db.Column(db.Boolean)
    ord = db.Column(db.Integer)
