# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_login import UserMixin, AnonymousUserMixin
from lightbbs import db, login_manager
from datetime import datetime
from .follow import Follow
from .message import Message
from .message_dialog import Message_dialog
from .notification import Notification
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for, request
from lightbbs.models.role import Role, Permission
import hashlib



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

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKAPP_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        self.followed.append(Follow(followed=self))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @property
    def password(self):
        raise ArithmeticError('密码属性不可访问')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expirathon=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expirathon)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id) \
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))