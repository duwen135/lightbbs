# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from . import tag, topic


class Tags_relation(db.Model):
    __tablename__ = 'lb_tags_relations'
    tag_id = db.Column(db.Integer, db.ForeignKey('lb_tags.id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('lb_topics.id'), primary_key=True)
