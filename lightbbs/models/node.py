# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Node(db.Model):
    __tablename__ = 'lb_nodes'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    content = db.Column(db.Text)
    keywords = db.Column(db.String(64))
    ico = db.Column(db.String(64))
    master_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    topic_num = db.Column(db.Integer)
