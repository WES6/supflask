# -*- coding: utf-8 -*-
from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import admin, db
from app.models import User


class LaView(ModelView):
    column_searchable_list = ['username']

    def is_accessible(self):
        if not current_user.is_authenticated():
            return False
        else:
            return current_user.username == ('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


admin.add_view(LaView(User, db.session))


class AnalyticsView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('an.html')


admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
