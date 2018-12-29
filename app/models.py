# coding: utf-8
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # role_id = db.Column(db.Integer)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property                                   # 设置password为只读
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter                            # 设置密码hash
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):        # 验证密码hash
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader                  # 是否登录验证
    def load_user(user_id):
        return User.query.get(int(user_id))
