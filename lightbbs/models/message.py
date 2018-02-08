# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Message(db.Model):
    __tablename__ = 'lb_messages'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    dialog_id = db.Column(db.Integer, unique=True)
    sender_uid = db.Column(db.Integer, unique=True)
    receiver_uid = db.Column(db.Integer, unique=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
