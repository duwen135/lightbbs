# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Notification(db.Model):
    __tablename__ = 'lb_notifications'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    topic_id = db.Column(db.Integer, unique=True)
    suid = db.Column(db.Integer, unique=True)
    nuid = db.Column(db.Integer, unique=True)
    ntype = db.Column(db.Integer)
    ntime = db.Column(db.DateTime)
