# -*- coding: utf-8; -*-
"""
Corporal Web Menus
"""

from tailbone import menus as base
from tailbone_corepos.menus import make_corepos_menu


class CorporalMenuHandler(base.MenuHandler):
    """
    Corporal menu handler
    """

    def make_menus(self, request, **kwargs):

        corepos_menu = make_corepos_menu(request)

        batch_menu = {
            'title': "Batches",
            'type': 'menu',
            'items': [
                {
                    'title': "CORE Member",
                    'route': 'batch.coremember',
                    'perm': 'batch.coremember.list',
                },
                {
                    'title': "Vendor Catalogs",
                    'route': 'vendorcatalogs',
                    'perm': 'vendorcatalogs.list',
                },
            ],
        }

        reports_menu = self.make_reports_menu(request, include_poser=True)

        other_menu = self.make_other_menu(request)

        admin_menu = self.make_admin_menu(request, include_stores=False)

        menus = [
            corepos_menu,
            batch_menu,
            reports_menu,
            other_menu,
            admin_menu,
        ]

        return menus

    def make_other_menu(self, request, **kwargs):
        return {
            'title': "Other",
            'type': 'menu',
            'items': [
                {
                    'title': "Generate New Project",
                    'route': 'generated_projects.create',
                    'perm': 'generated_projects.create',
                },
            ],
        }
