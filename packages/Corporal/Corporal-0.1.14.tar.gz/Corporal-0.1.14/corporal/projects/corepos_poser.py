# -*- coding: utf-8; -*-
"""
CORE-POS "Poser" project generator
"""

import os

import colander

from rattail.projects import ProjectGenerator


class COREPOSPoserProjectGenerator(ProjectGenerator):
    """
    Generator for CORE-POS "Poser" projects
    """
    key = 'corepos_poser'

    def make_schema(self, **kwargs):
        schema = super(COREPOSPoserProjectGenerator, self).make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='organization',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='org_slug',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='has_office_plugins',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_lane_plugins',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='use_posterior',
                                       typ=colander.Boolean()))

        return schema

    def normalize_context(self, context):
        context = super(COREPOSPoserProjectGenerator, self).normalize_context(context)

        # org_studly_prefix
        context['org_studly_prefix'] = context['org_slug'].capitalize()

        # requires
        requires = [('wikimedia/composer-merge-plugin', '^2.1')]
        if context['use_posterior']:
            requires.append(('rattail/posterior', '^0.1.1'))
        context['requires'] = requires

        return context

    def generate_project(self, output, context, **kwargs):

        ##############################
        # project root
        ##############################

        self.generate('gitignore',
                      os.path.join(output, '.gitignore'))

        self.generate('composer.json.mako',
                      os.path.join(output, 'composer.json'),
                      context)

        ##############################
        # office plugins
        ##############################

        if context['has_office_plugins']:

            office_plugins = os.path.join(output, 'office_plugins')
            os.makedirs(office_plugins)

            plugin_name = f"{context['org_studly_prefix']}Demo"
            demo_plugin = os.path.join(office_plugins, plugin_name)
            os.makedirs(demo_plugin)

            self.generate('office_plugins/PoserDemo/PoserDemo.php.mako',
                          os.path.join(demo_plugin, f"{plugin_name}.php"),
                          context)

            self.generate('office_plugins/PoserDemo/PoserDemoTask.php.mako',
                          os.path.join(demo_plugin, f"{plugin_name}Task.php"),
                          context)

        ##############################
        # lane plugins
        ##############################

        if context['has_lane_plugins']:

            lane_plugins = os.path.join(output, 'lane_plugins')
            os.makedirs(lane_plugins)

            demo_plugin = os.path.join(lane_plugins, 'PoserDemo')
            os.makedirs(demo_plugin)

            self.generate('lane_plugins/PoserDemo/PoserDemo.php',
                          os.path.join(demo_plugin, 'PoserDemo.php'))
