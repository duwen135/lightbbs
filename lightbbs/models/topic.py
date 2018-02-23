# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime
from lightbbs.exceptions import ValidationError
from flask import url_for
from markdown import markdown
import bleach
from lightbbs.models.user import User


class Topic(db.Model):
    __tablename__ = 'lb_topics'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('lb_nodes.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    last_reply_id = db.Column(db.Integer, db.ForeignKey('lb_users.id'))
    title = db.Column(db.String(64))
    keywords = db.Column(db.String(64))
    content = db.Column(db.Text)
    addtime = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, default=datetime.utcnow())
    last_reply = db.Column(db.DateTime, default=datetime.utcnow())
    views = db.Column(db.Integer)
    comment_num = db.Column(db.Integer)
    favorite_num = db.Column(db.Integer)
    is_close_comment = db.Column(db.Boolean)
    is_top = db.Column(db.Boolean)
    is_hidden = db.Column(db.Boolean)
    ord = db.Column(db.Integer)

    comments = db.relationship('Comment', backref='topic', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='topic', lazy='dynamic')
    notifications = db.relationship('Notification', backref='topic', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('文章没有内容。')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)
