# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import md5
import base64
from datetime import datetime

from flask import (
    views, request, render_template,
    redirect, url_for, flash,
    Blueprint, session,
    current_app as app)
from flask.helpers import locked_cached_property
from flask.ext.wtf import Form
from werkzeug.exceptions import Forbidden
from wtforms import fields, validators, ValidationError
from wtforms.fields import html5

from transflow.core.engines import mail, db, redis
from transflow.core.signature import shake, decrypt
from transflow.core.decorators import login_required
from transflow.core.tokens import AccessToken
from transflow.blueprints import blueprint_www
from transflow.rules.validators import PinyinLength
from transflow.models import UserModel, EmailTempModel


blueprint = Blueprint('account', __name__)
blueprint_www.register_blueprint(blueprint, url_prefix='/account')


class FillEmailView(views.MethodView):

    template = 'account/fill_email.html'

    class FillEmailForm(Form):
        email = html5.EmailField(
            'email', validators=[validators.Required()])

        def validate_email(self, field):
            email = field.data
            user = (UserModel.query
                    .filter(UserModel.email_insensitive == email)
                    .first())
            if user:
                raise ValidationError('邮箱已经被人抢注了')

    def get(self):
        form = self.FillEmailForm()
        return render_template(self.template, form=form)

    def error(self, form):
        return render_template(self.template, form=form), 400

    def post(self):
        form = self.FillEmailForm(request.values)
        if not form.validate():
            return self.error(form)
        email = form.email.data
        random_code = base64.b32encode(os.urandom(20))
        email_temp = EmailTempModel(email=email, random_code=random_code)
        db.session.add(email_temp)
        db.session.commit()
        self.send_email(email_temp=email_temp)
        flash('验证邮件已经发送到您的邮箱，请查收')
        return redirect(url_for('.fill'))

    def send_email(self, email_temp):
        mail.send(email_temp.email, 'validate_email', email_temp=email_temp)


class ConfirmEmailView(views.MethodView):

    class ConfirmEmailForm(Form):
        email = html5.EmailField(
            'email', validators=[validators.Required()])
        random_code = fields.StringField(
            'random_code', validators=[validators.Required()])

        def validate(self):
            et = self.email_temp
            if not et:
                raise ValidationError('非法的验证请求')

        @locked_cached_property
        def email_temp(self):
            return (
                EmailTempModel.query
                .filter(EmailTempModel.email == self.email.data)
                .filter(EmailTempModel.random_code == self.random_code.data)
                .first())

    def dispatch_request(self):
        form = self.ConfirmEmailForm(request.values, csrf_enabled=False)
        if not form.validate():
            raise Forbidden('非法的验证请求')
        email_temp = form.email_temp
        flash('邮箱验证已通过，继续注册流程')
        return redirect(url_for('.register', eid=email_temp.id))


class RSAFormMixin(object):
    form_id = fields.StringField(
        '表单ID',
        validators=[validators.Required()])
    pubkey = fields.StringField(
        '公钥',
        validators=[validators.Required()])

    RSA_PREFIX = 'RSA-FORM-KEY'

    @locked_cached_property
    def privkey(self):
        form_id = self.form_id.data
        pubkey = self.pubkey.data
        rsakey = '%s:%s:%s' % (self.RSA_PREFIX, form_id, pubkey)
        privkey = redis.get(rsakey)
        return privkey

    def validate_pubkey(self, field):
        if not self.privkey:
            raise ValidationError('表单已过期')

    def process(self, formdata=None, obj=None, **kwargs):
        if not self.is_submitted():
            form_id = base64.b32encode(os.random(20))
            pubkey, privkey = shake()
            rsakey = '%s:%s:%s' % (self.RSA_PREFIX, form_id, pubkey)
            redis.setex(rsakey, 600, privkey)
            kwargs.update(form_id=form_id, pubkey=pubkey)
        super(RSAFormMixin, self).process(
            formdata=formdata, obj=obj, **kwargs)


class RSAPasswordFormMixin(RSAFormMixin):
    password_encrypt = fields.PasswordField(
        '加密密码',
        validators=[validators.Required()])

    salt = app.config['SALT_ACCOUNT_PASSWORD']

    @locked_cached_property
    def password_hash(self):
        password = decrypt(self.password_encrypt.data, self.privkey)
        return md5(password + self.salt)


def make_login(response, user, permanent=True):
    access_token = AccessToken.generate()
    AccessToken.set(access_token, user.id)
    session.permanent = permanent
    if permanent:
        max_age = int(app.permanent_session_lifetime.total_seconds())
    else:
        max_age = None
    session['user_id'] = user.id
    session['access_token'] = access_token
    response.set_cookie('transflow_user_id', user.id, max_age)
    response.set_cookie('transflow_access_token', access_token, max_age)


class RegisterView(views.MethodView):

    template = 'account/register.html'

    class RegisterForm(Form, RSAPasswordFormMixin):
        realname = fields.StringField(
            '姓名',
            validators=[validators.Required(),
                        PinyinLength(min=2)])
        gender = fields.RadioField(
            '性别',
            choices=[('male', '男'), ('female', '女'), ('unknown', '不明')],
            validators=[validators.Required()])
        introduction = fields.StringField(
            '介绍',
            validators=[validators.Required()])

    def get(self, eid):
        et = EmailTempModel.query.get(eid)
        if not et:
            raise Forbidden('邮箱已经被抢注了')
        form = self.RegisterForm()
        return render_template(self.template, form=form, email_temp=et)

    def error(self, et, form):
        return render_template(self.template, form=form, email_temp=et), 400

    def post(self, eid):
        et = EmailTempModel.query.get(eid)
        if not et:
            raise Forbidden('邮箱已经被抢注了')
        form = self.RegisterForm(request.values)
        if not form.validate():
            return self.error(et, form)
        realname = form.realname.data
        gender = form.gender.data
        introduction = form.introduction.data
        password_hash = form.password_hash
        user = UserModel.create(
            realname=realname,
            gender=gender,
            introduction=introduction,
            email=et.email,
            password_hash=password_hash)
        flash('注册成功')
        response = redirect(url_for('home.index'))
        make_login(response, user)
        return response


class LoginView(views.MethodView):

    template = 'account/login.html'

    class LoginForm(Form, RSAPasswordFormMixin):
        email = html5.EmailField(
            'email', validators=[validators.Required()])

        def validate(self):
            super(LoginForm, self).validate()  # noqa
            if not self.user:
                raise ValidationError('邮箱不存在')
            if self.user.password_hash != self.password_hash:
                raise ValidationError('密码错误')

        @locked_cached_property
        def user(self):
            email = self.email.data
            user = (
                UserModel.query
                .filter(UserModel.email_insensitive == email)
                .first())
            return user

    def get(self):
        form = self.LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = self.LoginForm(request.form)
        if not form.validate():
            return self.error(form)
        user = form.user
        user.date_last_signed_in = datetime.now()
        db.session.commit()
        flash('登录成功')
        response = redirect(url_for('home.index'))
        make_login(response, user)
        return response

    def error(self, form):
        return render_template(self.template, form=form), 400


class ChangePasswordView(views.MethodView):

    template = 'account/change_password.html'

    class ChangePasswordForm(Form, RSAPasswordFormMixin):
        new_password_encrypt = fields.PasswordField(
            '加密新密码',
            validators=[validators.Required()])

        @locked_cached_property
        def new_password_hash(self):
            new_password = decrypt(
                self.new_password_encrypt.data, self.privkey)
            return md5(new_password + self.salt)

        def validate(self):
            super(ChangePasswordForm, self).validate()  # noqa
            if self.user.password_hash != self.password_hash:
                raise ValidationError('密码不正确')

        @locked_cached_property
        def user(self):
            return UserModel.query.get(request.user_id)

    @login_required
    def get(self):
        form = self.ChangePasswordForm()
        return render_template(self.template, form=form)

    def error(self, form):
        return render_template(self.template, form=form)

    @login_required
    def post(self):
        form = self.ChangePasswordForm(request.form)
        if not form.validate():
            return self.error(form)
        user = form.user
        user.password_hash = form.new_password_hash
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('home.index'))


blueprint.add_url_rule(
    '/fill_email',
    view_func=FillEmailView.as_view(b'fill_email'))
blueprint.add_url_rule(
    '/confirm_email',
    view_func=ConfirmEmailView.as_view(b'confirm_email'))
blueprint.add_url_rule(
    '/register',
    view_func=RegisterView.as_view(b'register'))
blueprint.add_url_rule(
    '/login',
    view_func=LoginView.as_view(b'login'))
blueprint.add_url_rule(
    '/change_password',
    view_func=RegisterView.as_view(b'change_password'))
