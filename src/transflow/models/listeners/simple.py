# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.hook import entity, CommonEntityHook
from transflow.models import (
    ProjectModel, StaffModel, MemberModel,
    TaskModel, CrossModel, DocumentModel)


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


@entity(TaskModel)
class TaskHook(CommonEntityHook):

    def on_flush(self, new_tasks, deleted_tasks):
        self.update_children_count(
            new_tasks | deleted_tasks,
            'project', 'tasks', 'tasks_count')


@entity(CrossModel)
class CrossHook(CommonEntityHook):

    def on_flush(self, new_crosses, deleted_crosses):
        self.update_children_count(
            new_crosses | deleted_crosses,
            'project', 'crosses', 'crosses_count')


@entity(DocumentModel)
class DocumentHook(CommonEntityHook):

    def on_flush(self, new_documents, deleted_documents):
        self.update_children_count(
            new_documents | deleted_documents,
            'project', 'documents', 'documents_count')
