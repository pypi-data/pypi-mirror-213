# -*- coding: utf-8; -*-
"""
Corporal project generator
"""

from rattail.projects import PoserProjectGenerator


class CorporalProjectGenerator(PoserProjectGenerator):
    """
    Generator for projects based on Corporal.
    """
    key = 'corporal'

    def normalize_context(self, context):

        # set these first
        context['has_db'] = True
        context['has_web'] = True
        context['alembic_version_locations'] = [
            'rattail.db:alembic/versions',
            'rattail_corepos.db:alembic/versions',
        ]
        context['mako_directories'] = [
            '{}.web:templates'.format(context['pkg_name']),
            'corporal.web:templates',
            'tailbone_corepos:templates',
            'tailbone:templates',
        ]

        # then do parent logic
        context = super(CorporalProjectGenerator, self).normalize_context(context)

        # add dependencies
        context['requires']['Corporal'] = True

        return context
