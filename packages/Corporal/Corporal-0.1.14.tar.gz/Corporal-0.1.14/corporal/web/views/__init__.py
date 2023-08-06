# -*- coding: utf-8; -*-
"""
Corporal Views
"""

from corporal.web.views import essentials


def includeme(config):
    essentials.defaults(config)
