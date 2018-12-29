# -*- coding: utf-8 -*-


class Config:
    # 密钥配置
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # 数据库ORM配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # admin语言配置
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    # admin 样式配置
    FLASK_ADMIN_SWATCH = 'cosmo'


class DevelopmentConfig(Config):
    DEBUG = True
    # 数据Url配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:000000@localhost:3306/alert'


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
