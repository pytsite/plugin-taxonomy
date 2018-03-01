"""PytSite Taxonomy Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _api, _model as model, _widget as widget
from . import _error as error
from ._api import register_model, is_model_registered, find, get, dispense, create, find_by_title, find_by_alias
from ._model import Term

from pytsite import semver as _semver


def plugin_load():
    from pytsite import lang
    from plugins import permissions, assetman

    # Permissions
    permissions.define_group('taxonomy', 'taxonomy@taxonomy')

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Assets
    assetman.js_module('taxonomy-widget-cloud', __name__ + '@js/taxonomy-widget-cloud')
    assetman.t_less(__name__)
    assetman.t_js(__name__)


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)


def plugin_load_wsgi():
    from pytsite import router, tpl
    from . import _controllers

    # Tpl resources
    tpl.register_package(__name__)

    # Search term route
    router.handle(_controllers.SearchTerms, '/taxonomy/search/<model>/<query>', 'taxonomy@search_terms')


def plugin_update(v_from: _semver.Version):
    if v_from < '2.7':
        from plugins import odm

        odm.reindex()
