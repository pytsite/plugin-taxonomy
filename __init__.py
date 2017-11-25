"""PytSite Taxonomy Plugin
"""
# Public API
from . import _api, _model as model, _widget as widget
from ._api import register_model, is_model_registered, find, dispense, find_by_title, find_by_alias

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import tpl, lang, router
    from plugins import assetman, permissions, admin
    from . import _controllers

    # Permissions
    permissions.define_group('taxonomy', 'taxonomy@taxonomy')

    # Language resources
    lang.register_package(__name__)

    # Tpl resources
    tpl.register_package(__name__)

    # Assetman resources
    assetman.register_package(__name__)
    assetman.js_module('taxonomy-widget-cloud', __name__ + '@js/taxonomy-widget-cloud')
    assetman.t_less(__name__ + '@css/**', 'css')
    assetman.t_js(__name__ + '@js/**', 'js')

    # Search term route
    router.handle(_controllers.SearchTerms(), '/taxonomy/search/<model>/<query>', 'taxonomy@search_terms')

    # Admin sidebar menu
    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500)


_init()
