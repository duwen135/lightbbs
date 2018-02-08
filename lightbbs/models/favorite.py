# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Favorite(db.Model):
    __tablename__ = 'lb_favorites'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer, unique=True)
    favorites = db.Column(db.Integer)
    content = db.Column(db.Text)
    reply_time = db.Column(db.DateTime)
