# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.hook import entity, CommonEntityHook
from transflow.models import (
    ProjectModel, StaffModel, MemberModel)

@entity(ProjectModel)
class ProjectHook(CommonEntityHook):

    def on_flush(self, new_projects, deleted_projects):
        self.update_children_count(
            new_projects | deleted_projects,
            'company', 'projects', 'projects_count')

@entity(StaffModel)
class StaffHook(CommonEntityHook):

    def on_flush(self, new_staffs, deleted_staffs):
        self.update_children_count(
            new_staffs | deleted_staffs,
            'company', 'staffs', 'staffs_count')

@entity(MemberModel)
class MemberHook(CommonEntityHook):

    def on_flush(self, new_members, deleted_members):
        self.update_children_count(
            new_members | deleted_members,
            'project', 'members', 'members_count')
