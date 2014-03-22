# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import request, views, Blueprint

from transflow.blueprints import blueprint_www
from transflow.core.decorators import login_required

blueprint = Blueprint('home', __name__)
blueprint_www.register_blueprint(blueprint)


class HomeView(views.MethodView):

    @login_required
    def get(self):
        return '受人尊敬的%s，欢迎你来到十五言' % request.user.realname


blueprint.add_url_rule(
    '/',
    view_func=HomeView.as_view(b'index'))
