# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


# 登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


# 登出路由
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('admin.index'))


# 注册路由
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successful register.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
