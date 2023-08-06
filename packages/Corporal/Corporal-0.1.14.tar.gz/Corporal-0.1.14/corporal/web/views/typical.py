# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Typical views for convenient includes
"""

from tailbone.views import typical as base


def defaults(config, **kwargs):
    mod = lambda spec: kwargs.get(spec, spec)

    # tailbone essentials
    config.include('tailbone.views.essentials')

    # tailbone typical
    kwargs['tailbone.views.batch.vendorcatalog'] = 'tailbone_corepos.views.batch.vendorcatalog'
    base.defaults(config, **kwargs)

    # tailbone extras
    config.include(mod('tailbone.views.poser'))

    # main views for CORE-POS
    config.include(mod('tailbone_corepos.views'))

    # batches
    config.include(mod('tailbone_corepos.views.batch.coremember'))

    # corporal-specific
    config.include(mod('corporal.web.views.supplemental'))


def includeme(config):
    defaults(config)
