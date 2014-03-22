# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint as _Blueprint

__all__ = ['Blueprint']


class Blueprint(_Blueprint):

    def register_blueprint(self, blueprint, **options):
        """Registers another nested blueprint on the blueprint.

        .. versionadded:: 0.10
        """
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (
                options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(
                blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)
