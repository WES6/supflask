# -*- coding: utf-8 -*-
import sys

from flask import Flask
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_moment import Moment

import config

# 解释器编码改为UTF-8
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config.from_object(config.config["default"])

# 数据库 ORM 扩展初始化
db = SQLAlchemy(app)
# admin 中文扩展初始化
babel = Babel(app)
# admin 插件初始化及配置
admin = Admin(app, name='Alert', template_mode='bootstrap3')
# moment 初始化
moment = Moment(app)
# login 插件初始化
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
# Bootstrap初始化
bootstrap = Bootstrap(app)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
