# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_login import UserMixin
from lightbbs import db
from datetime import datetime
from .follow import Follow
from .message import Message
from .message_dialog import Message_dialog
from .notification import Notification

class User(UserMixin,db.Model):
    __tablename__ = 'lb_users'
    # 基本信息
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(64))
    homepage = db.Column(db.String(64))
    location = db.Column(db.String(64))
    signature = db.Column(db.Text)
    about_me = db.Column(db.Text)

    # 统计信息
    topic_num = db.Column(db.Integer)
    replie_num = db.Column(db.Integer)
    notice_num = db.Column(db.Integer)
    follow_num = db.Column(db.Integer)
    faorite_num = db.Column(db.Integer)
    messages_unread = db.Column(db.Integer)
    integral = db.Column(db.Integer)

    #更多信息
    confirmed = db.Column(db.Boolean, default=False)
    regtime = db.Column(db.DateTime, default=datetime.utcnow())
    lastlogin = db.Column(db.DateTime, default=datetime.utcnow())
    lastpost = db.Column(db.DateTime,default=datetime.utcnow())
    ip = db.Column(db.String(64))
    is_active = db.Column(db.Boolean)

    #外键&关系
    role_id = db.Column(db.Integer, db.ForeignKey('lb_roles.id'))

    nodes = db.relationship('Node', backref='master', lazy='dynamic')
    topics_sender = db.relationship('Topic', backref='topic_sender', lazy='dynamic')
    topic_last_replies = db.relationship('Topic', backref='topic_last_remly', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')
    follower = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    senders = db.relationship('Message', foreign_keys=[Message.sender_id],
                              backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    receivers = db.relationship('Message', foreign_keys=[Message.receiver_id],
                                backref=db.backref('receiver', lazy='joined'), lazy='dynamic')
    dialog_senders = db.relationship('Message_dialog', foreign_keys=[Message_dialog.sender_id],
                                     backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    dialog_receivers = db.relationship('Message_dialog', foreign_keys=[Message_dialog.receiver_id],
                                     backref=db.backref('receiver', lazy='joined'), lazy='dynamic')
    comments_by = db.relationship('Notification', foreign_keys=[Notification.comment_by],
                                  backref=db.backref('comment_by', lazy='joined'), lazy='dynamic')
    topics_sender_id = db.relationship('Notification', foreign_keys=[Notification.topic_sender_id],
                                       backref=db.backref('topic_sender_id', lazy='joined'), lazy='dynamic')

