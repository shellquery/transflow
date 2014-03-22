# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyquery import PyQuery

from flask import render_template
from flask.ext.mail import Message

from transflow.core.engines import mail


def send(recipients, key, **context):
    if isinstance(recipients, basestring):
        recipients = [recipients]
    template = 'email/%s' % key
    html = render_template(template, **context)
    pq = PyQuery(str(html))
    title = pq('title').html()
    content = pq('content').html()
    msg = Message(title, recipients=recipients)
    msg.html = content
    mail.send(msg)
