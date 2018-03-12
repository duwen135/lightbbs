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
from .role import Role, Permission
import hashlib
from .topic import Topic
from .favorite import Favorite


class User(UserMixin,db.Model):
    __tablename__ = 'lb_users'
    # 基本信息
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True) #邮箱
    username = db.Column(db.String(64), unique=True, index=True) #用户名
    password_hash = db.Column(db.String(128)) #密码序列值
    avatar = db.Column(db.String(64)) #头像地址
    avatar_hash = db.Column(db.String(64)) #头像序列值
    homepage = db.Column(db.String(64)) #用户网站
    location = db.Column(db.String(64)) #用户地址
    signature = db.Column(db.Text) #签名
    about_me = db.Column(db.Text) #关于我

    # 统计信息
    topic_num = db.Column(db.Integer) #该用户发布的话题数量
    replie_num = db.Column(db.Integer) #该用户的回复数量
    notice_num = db.Column(db.Integer) #该用户的通知数量
    follow_num = db.Column(db.Integer) #该用户的粉丝数量
    faorite_num = db.Column(db.Integer) #该用户收藏的话题数量
    messages_unread = db.Column(db.Integer) #未读信息数量
    integral = db.Column(db.Integer) #积分

    #更多信息
    confirmed = db.Column(db.Boolean, default=False) #该用户是否认证
    regtime = db.Column(db.DateTime, default=datetime.utcnow) #该用户的注册时间
    lastlogin = db.Column(db.DateTime) #该用户最后的登录时间
    lastpost = db.Column(db.DateTime) #该用户最后发布话题时间
    ip = db.Column(db.String(64)) #该用户的ip地址
    is_active = db.Column(db.Boolean, default=True) #该用户是否激活

    #外键&关系
    role_id = db.Column(db.Integer, db.ForeignKey('lb_roles.id'))

    nodes = db.relationship('Node', backref='master', lazy='dynamic')
    sender_topics = db.relationship('Topic', foreign_keys=[Topic.sender_id], backref='sender', lazy='dynamic')
    last_topic_replies = db.relationship('Topic',foreign_keys=[Topic.last_reply_id], backref='reply', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followeds = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    sender_messages = db.relationship('Message', foreign_keys=[Message.sender_id],
                              backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    receiver_messages = db.relationship('Message', foreign_keys=[Message.receiver_id],
                                backref=db.backref('receiver', lazy='joined'), lazy='dynamic')
    sender_dialogs = db.relationship('Message_dialog', foreign_keys=[Message_dialog.sender_id],
                                     backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    receiver_dialogs = db.relationship('Message_dialog', foreign_keys=[Message_dialog.receiver_id],
                                     backref=db.backref('receiver', lazy='joined'), lazy='dynamic')
    comments_by = db.relationship('Notification', foreign_keys=[Notification.comment_by],
                                  backref=db.backref('commenter', lazy='joined'), lazy='dynamic')
    topics_sender_id = db.relationship('Notification', foreign_keys=[Notification.topic_sender_id],
                                       backref=db.backref('sender', lazy='joined'), lazy='dynamic')

    #生成虚拟用户
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
                     homepage=forgery_py.internet.domain_name(),
                     location=forgery_py.address.city(),
                     signature=forgery_py.lorem_ipsum.sentence(),
                     about_me=forgery_py.lorem_ipsum.paragraph(),
                     regtime=forgery_py.date.datetime(True),
                     ip=forgery_py.internet.ip_v4())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    #用户自关注
    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    #初始化用户角色和头像
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['LIGHTBBS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        self.followeds.append(Follow(followed=self))

    #登录回调
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #密码的只写属性、验证密码
    @property
    def password(self):
        raise ArithmeticError('密码属性不可访问')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    #生成认证码、认证函数
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

    #重设密码的生成认证码和认证函数
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

    #修改邮箱的生成认证码和认证函数
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

    #权限判断函数和管理员账户判断函数
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #更新用户最近登录时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    #用户头像生成
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    #用户关注、取消关注、是否关注中、是否被关注
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followeds.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followeds.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    # 收藏、取消搜藏、是否已收藏
    def favorite(self, topic):
        if not self.is_favoriting(topic):
            fv = Favorite(user=self, topic=topic)
            db.session.add(fv)

    def unfavorite(self, topic):
        fv = self.favorites.filter_by(topic_id=topic.id).first()
        if fv:
            db.session.delete(fv)

    def is_favoriting(self, topic):
        return self.favorites.filter_by(
            topic_id=topic.id).first() is not None


    #关注用户的文章
    @property
    def followed_topics(self):
        #from .topic import Topic
        return Topic.query.join(Follow, Follow.followed_id == Topic.sender_id).filter(Follow.follower_id == self.id)
    '''
    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'regtime': self.regtime,
            'lastlogin': self.lastlogin,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user
    '''
    '''
    #生成认证口令和验证认证口令
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
    '''

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