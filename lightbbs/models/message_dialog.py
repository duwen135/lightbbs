# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Message_dialog(db.Model):
    __tablename__ = 'lb_message_dialogs'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    sender_uid = db.Column(db.Integer, unique=True)
    receiver_uid = db.Column(db.Integer, unique=True)
    last_content = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    sender_remove = db.Column(db.Boolean)
    receiver_remove = db.Column(db.Boolean)
    sender_read = db.Column(db.Boolean)
    recerver_read = db.Column(db.Boolean)
    messages = db.Column(db.Integer)
