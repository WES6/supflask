# -*- coding: utf-8 -*-
import jieba as jieba
import requests
from bs4 import BeautifulSoup
from flask import url_for, request, flash
from flask_admin import BaseView, expose
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from wtforms import StringField

from app import admin, db
from app.models import User, Alert


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


# class AlertView(ModelView):
#     @expose('/')
#     @login_required
#     def index(self):
#         return self.render('alert/alert.html')

class al_BrandForm(BaseForm):
    al_name = StringField()


class AlertView(ModelView):
    column_searchable_list = ['al_name']

    def is_accessible(self):
        return current_user.is_authenticated

    column_display_pk = True
    # column_list = ('id', 'abbreviation', 'company_name')

    column_labels = {
        'al_name': u'敏感词'
    }

    # 覆写form
    form = al_BrandForm

    def create_model(self, form):
        try:
            model = self.model()
            # populate_obj 便捷赋值方法
            form.populate_obj(model)

            alert_st = form.al_name._value()
            baidu_url = "https://www.baidu.com/s?wd=" + alert_st
            supheader = {"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
            re = requests.get(baidu_url, headers=supheader)
            soup = BeautifulSoup(re.text, "lxml")
            urls = []
            nums = 0
            for item in soup.find_all(class_="t"):
                if len(item.find("a").attrs["href"]) > 255:
                    continue
                print(len(item.find("a").attrs["href"]))
                urls.append(item.find("a").attrs["href"])

            model.al_1 = urls[0]
            try:
                re1 = requests.get(urls[0], timeout=2)
                words = jieba.lcut(re1.text)
                for word in words:
                    if word == alert_st:
                        nums += 1
            except:
                pass
            model.al_2 = urls[1]
            try:
                re1 = requests.get(urls[1], timeout=2)
                words = jieba.lcut(re1.text)
                for word in words:
                    if word == alert_st:
                        nums += 1
            except:
                pass
            model.al_3 = urls[2]
            try:
                re1 = requests.get(urls[2], timeout=2)
                words = jieba.lcut(re1.text)
                for word in words:
                    if word == alert_st:
                        nums += 1
            except:
                pass
            model.al_4 = urls[3]
            try:
                re1 = requests.get(urls[3], timeout=2)
                words = jieba.lcut(re1.text)
                for word in words:
                    if word == alert_st:
                        nums += 1
            except:
                pass
            model.al_5 = urls[4]
            try:
                re1 = requests.get(urls[4], timeout=2)
                words = jieba.lcut(re1.text)
                for word in words:
                    if word == alert_st:
                        nums += 1
            except:
                pass
            model.al_num = nums
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')

            self.session.rollback()

            return False
        return model


admin.add_view(AlertView(Alert, db.session))
# name='Alert', endpoint='alert'
