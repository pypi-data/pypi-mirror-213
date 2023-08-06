# -*- coding: utf-8; -*-
"""
Project views
"""

from tailbone.views import ViewSupplement


class GeneratedProjectViewSupplement(ViewSupplement):
    """
    View supplement for generating projects
    """
    route_prefix = 'generated_projects'

    def configure_form_corepos_poser(self, f):

        f.set_grouping([
            ("Naming", [
                'organization',
                'org_slug',
            ]),
            ("Options", [
                'has_office_plugins',
                'has_lane_plugins',
                'use_posterior',
            ]),
        ])

        # organization
        f.set_helptext('organization', "For use with branding etc.")
        f.set_default('organization', "Acme Foods Co-op")

        # org_slug
        f.set_helptext('org_slug', "Short name used for folders etc.")
        f.set_default('org_slug', 'acmefoods')

        # has_*_plugins
        f.set_label('has_office_plugins', "Office Plugins")
        f.set_default('has_office_plugins', True)
        f.set_label('has_lane_plugins', "Lane Plugins")
        f.set_default('has_lane_plugins', False)

        # use_posterior
        f.set_helptext('use_posterior', "Set this if you plan to integrate with Tailbone API")
        f.set_default('use_posterior', False)

    def configure_form_corporal(self, f):

        f.set_grouping([
            ("Naming", [
                'name',
                'pkg_name',
                'pypi_name',
                'organization',
            ]),
            ("Core", [
                'extends_config',
                'has_cli',
            ]),
            ("Database", [
                'extends_db',
            ]),
        ])

        # default settings
        f.set_default('extends_config', False)
        f.set_default('extends_db', False)


def includeme(config):
    GeneratedProjectViewSupplement.defaults(config)
