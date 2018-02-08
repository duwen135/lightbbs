# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Node(db.Model):
    __tablename__ = 'lb_nodes'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    pid = db.Column(db.Integer, unique=True)
    cname = db.Column(db.String(64))
    content = db.Column(db.Text)
    keywords = db.Column(db.String(64))
    ico = db.Column(db.String(64))
    master = db.Column(db.Integer, unique=True)
    permit = db.Column(db.String(64))
    listnum = db.Column(db.Integer)
    clevel = db.Column(db.String(64))
    cord = db.Column(db.Integer)
