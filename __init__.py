"""PytSite Taxonomy Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _model as model, _widget as widget
from . import _error as error
from ._api import register_model, is_model_registered, find, dispense, get
from ._model import Term

# Locally needed imports
from semaver import Version as _Version


def plugin_load():
    from plugins import permissions

    # Permissions
    permissions.define_group('taxonomy', 'taxonomy@taxonomy')


def plugin_load_wsgi():
    from pytsite import router
    from plugins import admin
    from . import _controllers

    # Search term route
    router.handle(_controllers.SearchTerms, '/taxonomy/search/<model>/<query>', 'taxonomy@search_terms')

    # Admin sidebar section
    admin.sidebar.add_section('taxonomy', 'taxonomy@taxonomy', 0, 'title')


def plugin_update(v_from: _Version):
    if v_from < '2.7':
        from plugins import odm

        odm.reindex()
