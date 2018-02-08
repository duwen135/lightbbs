# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Topic(db.Model):
    __tablename__ = 'lb_topics'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    node_id = db.Column(db.Integer, unique=True)
    uid = db.Column(db.Integer, unique=True)
    ruid = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(64))
    keywords = db.Column(db.String(64))
    content = db.Column(db.Text)
    addtime = db.Column(db.DateTime)
    updatetime = db.Column(db.DateTime)
    lastreply = db.Column(db.DateTime)
    views = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    closecomment = db.Column(db.Boolean)
    is_top = db.Column(db.Boolean)
    is_hidden = db.Column(db.Boolean)
    ord = db.Column(db.Integer)
