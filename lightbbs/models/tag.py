# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db

tags_relation = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('lb_tags.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('lb_topics.id'))
)

class Tag(db.Model):
    __tablename__ = 'lb_tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64))
    topic_num = db.Column(db.Integer)

    topics = db.relationship('Tags_relation', secondary=tags_relation, backref='tag', lazy='dynamic')
