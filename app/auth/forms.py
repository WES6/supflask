# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('password', validators=[Required()])
    # flask_login提供快捷记住我cookie保存
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    username = StringField('Username', validators=[
        Required(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
