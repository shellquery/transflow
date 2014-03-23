# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.helpers import locked_cached_property
from flask.wrappers import Request


class TransflowRequest(Request):

    @locked_cached_property
    def user_id(self):
        return self.user.get('id')

    @locked_cached_property
    def user(self):
        from transflow.core.users import user_meta
        from transflow.core.tokens import AccessToken
        user_id = self.cookies.get('sign_in_user_id')
        access_token = self.cookies.get('sign_in_access_token')
        if not user_id or not access_token:
            return {}
        if user_id != AccessToken.get(access_token):
            return {}
        user = user_meta(user_id)
        return user
