# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db

tags_relation = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('lb_tags.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('lb_topics.id'))
)

class Tag(db.Model):
    __tablename__ = 'lb_tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64))
    topic_num = db.Column(db.Integer)

    topics = db.relationship('Topic', secondary=tags_relation, backref=db.backref('tags', lazy=True), lazy='dynamic')


    # 生成虚拟用户
    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            tg = Tag(tog_name=forgery_py.lorem_ipsum.word())
            db.session.add(tg)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()