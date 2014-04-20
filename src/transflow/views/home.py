# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import views, Blueprint, render_template

from transflow.blueprints import blueprint_www

blueprint = Blueprint('home', __name__)
blueprint_www.register_blueprint(blueprint)


class HomeView(views.MethodView):
    template = 'index.html'

    def get(self):
        return render_template(self.template)


class ContactView(views.MethodView):
    template = 'contact.html'

    def get(self):
        return render_template(self.template)


blueprint.add_url_rule(
    '/',
    view_func=HomeView.as_view(b'index'))
blueprint.add_url_rule(
    '/contact/',
    view_func=ContactView.as_view(b'contact'))
