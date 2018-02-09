# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'lb_messages'
    id = db.Column(db.Integer, primary_key=True)
    dialog_id = db.Column(db.Integer, db.ForeignKey('lb_message_dialogs.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
