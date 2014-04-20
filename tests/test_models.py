# -*- coding: utf-8 -*
from __future__ import unicode_literals

from transflow.core.engines import db

from .transflow_testing import TestCase
from .transflow_testing import (
    add_user, add_company, add_company_project, add_project_task,
    add_project_cross, add_project_document, add_cross_document,
    add_project_member, add_company_staff, connect_ct, connect_tc)


class ModelTestCase(TestCase):

    def setUp(self):
        super(ModelTestCase, self).setUp()
        self.user = user = add_user()
        db.session.commit()
        self.company = company = add_company(admin_user=user)
        self.project = project = add_company_project(company, manage_user=user)
        self.member = add_project_member(project, user)
        self.staff = add_company_staff(company, user)
        db.session.commit()
        self.assertEquals(self.project.members.count(), 1)
        self.assertEquals(self.project.members_count, 1)
        self.assertEquals(self.company.projects.count(), 1)
        self.assertEquals(self.company.projects_count, 1)
        self.assertEquals(self.company.staffs.count(), 1)
        self.assertEquals(self.company.staffs_count, 1)

    def test_orgnization(self):
        user2 = add_user(email='test2@gmail.com')
        db.session.commit()
        add_company_staff(self.company, user2)
        db.session.commit()
        self.assertEquals(self.company.staffs.count(), 2)
        self.assertEquals(self.company.staffs_count, 2)

    def test_sequence_task(self):
        task1 = add_project_task(self.project, self.user, name='test1')
        task2 = add_project_task(self.project, self.user, name='test2')
        task3 = add_project_task(self.project, self.user, name='test3')
        cross1 = add_project_cross(self.project, is_start=True)
        cross2 = add_project_cross(self.project)
        cross3 = add_project_cross(self.project)
        cross4 = add_project_cross(self.project, is_end=True)
        connect_ct(cross1, task1)
        connect_tc(task1, cross2)
        connect_ct(cross2, task2)
        connect_tc(task2, cross3)
        connect_ct(cross3, task3)
        connect_tc(task3, cross4)
        document1 = add_project_document(self.project)
        document2 = add_project_document(self.project)
        add_cross_document(cross1, document1)
        add_cross_document(cross1, document2)
        db.session.commit()
        self.assertEquals(self.project.tasks_count, 3)
        self.assertEquals(self.project.crosses_count, 4)
        self.assertEquals(self.project.documents_count, 2)
