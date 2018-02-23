# -*- coding:utf-8 -*-
__author__ = 'duwen'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LIGHTBBS_MAIL_SUBJECT_PREFIX = '[Lightbbs]'
    LIGHTBBS_MAIL_SENDER = 'Lightbbs Admin <lightbbs@example.com>'
    LIGHTBBS_ADMIN = os.environ.get('LIGHTBBS_ADMIN')
    LIGHTBBS_POSTS_PER_PAGE = 20
    LIGHTBBS_FOLLOWERS_PER_PAGE = 50
    LIGHTBBS_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-tset.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'tseting': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
