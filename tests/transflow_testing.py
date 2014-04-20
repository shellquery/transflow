# -*- coding: utf-8 -*
from __future__ import unicode_literals

import os

from flask.ext.testing import TestCase as _TestCase

from transflow import app
from transflow.core.engines import db

from transflow.models import (
    UserModel, CompanyModel, ProjectModel,
    MemberModel, StaffModel, CrossModel,
    TaskModel, DocumentModel)


def add_user(realname='test', email='test@gmail.com'):
    user = UserModel(
        realname=realname,
        email=email,
        password_hash='*' * 40,
        gender='male')
    db.session.add(user)
    return user


def add_company(admin_user, name='test'):
    company = CompanyModel(
        admin_user_id=admin_user.id,
        name=name)
    db.session.add(company)
    return company


def add_company_project(company, manage_user, name='test'):
    project = ProjectModel(
        manage_user_id=manage_user.id,
        name=name)
    company.projects.append(project)
    return project


def add_company_staff(company, user):
    staff = StaffModel(
        user_id=user.id)
    company.staffs.append(staff)
    return staff


def add_project_member(project, user):
    member = MemberModel(
        user_id=user.id)
    project.members.append(member)
    return member


def add_project_cross(project, is_start=False, is_end=False):
    cross = CrossModel(
        is_start=is_start,
        is_end=is_end)
    project.crosses.append(cross)
    return cross


def add_project_document(project, name='test', url='http://test'):
    document = DocumentModel(
        name=name,
        url=url)
    project.documents.append(document)
    return document


def add_cross_document(cross, document):
    cross.documents.append(document)


def add_project_task(project, user, name='test'):
    task = TaskModel(
        user_id=user.id,
        name=name)
    project.tasks.append(task)
    return task


def connect_ct(cross, task):
    cross.down_tasks.append(task)


def connect_tc(task, cross):
    task.down_crosses.append(cross)


class TestCase(_TestCase):

    def create_app(self):
        self.db_path = db_path = '/tmp/transflow.db'
        test_config = dict(
            SQLALCHEMY_DATABASE_URI='sqlite:///%s' % db_path,
            TESTING=True,
            WTF_CSRF_ENABLED=False
        )
        try:
            os.unlink(self.db_path)
        except OSError:
            pass
        app.config.update(test_config)
        return app

    def setUp(self):
        db.create_all()
        from transflow.models import generators

        def mock_nextorigid(self, key):
            orig_id = mock_nextorigid.func_dict.setdefault(key, 1)
            mock_nextorigid.func_dict[key] += 1
            return orig_id
        generators.nextorigid = lambda key: mock_nextorigid(generators, key)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.unlink(self.db_path)
