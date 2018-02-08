# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Stat(db.Model):
    __tablename__ = 'lb_stats'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    item = db.Column(db.String(64))
    value = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)
