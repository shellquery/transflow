# -*- coding: utf-8 -*
from __future__ import unicode_literals

from transflow.core.engines import db

from .transflow_testing import TestCase
from .transflow_testing import (
    add_user, add_company, add_company_project, add_project_task,
    add_project_cross, add_project_document, add_cross_document,
    add_project_member, add_company_staff, connect_ct, connect_tc)

from transflow.models import StaffModel

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
