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

    topics = db.relationship('Topic', backref='node', lazy='dynamic')

    # 生成虚拟用户
    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py
        from .user import User

        seed()
        user_count = User.query.count()
        node_count = Node.query.count()
        for i in range(count):
            nd = Node.query.offset(randint(0, node_count)).first()
            u = User.query.offset(randint(0, user_count - 1)).first()
            if nd:
                n = Node(parent_id=nd.id,
                         name=forgery_py.lorem_ipsum.word(),
                         content=forgery_py.lorem_ipsum.paragraph(),
                         master=u)
            else:
                n = Node(parent_id=0,
                         name=forgery_py.lorem_ipsum.word(),
                         content=forgery_py.lorem_ipsum.paragraph(),
                         master=u)

            db.session.add(n)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
