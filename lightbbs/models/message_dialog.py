# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Message_dialog(db.Model):
    __tablename__ = 'lb_message_dialogs'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    last_content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime)
    sender_remove = db.Column(db.Boolean)
    receiver_remove = db.Column(db.Boolean)
    sender_read = db.Column(db.Boolean)
    recerver_read = db.Column(db.Boolean)
    message_num = db.Column(db.Integer)

    messages = db.relationship('Message', backref='dialog', lazy='dynamic')
