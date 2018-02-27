# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime
from flask import url_for
from markdown import markdown
import bleach
from lightbbs.exceptions import ValidationError


class Comment(db.Model):
    __tablename__ = 'lb_comments'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('lb_topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow())

    '''
    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)
    '''


