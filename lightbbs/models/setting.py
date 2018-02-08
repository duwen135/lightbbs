# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Setting(db.Model):
    __tablename__ = 'lb_settings'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(64))
    value = db.Column(db.Text)
    type = db.Column(db.Integer)
