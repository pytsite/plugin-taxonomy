"""PytSite Taxonomy Plugin.
"""
# Public API
from . import _api, _model as model, _widget as widget
from ._api import register_model, is_model_registered, find, dispense, build_alias_str, find_by_title, \
    find_by_alias

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, tpl, lang, router, admin, permissions

    # Permissions
    permissions.define_group('taxonomy', 'taxonomy@taxonomy')

    # Resources
    lang.register_package(__name__, alias='taxonomy')
    tpl.register_package(__name__, alias='taxonomy')
    assetman.register_package(__name__, alias='taxonomy')

    # Search term route
    router.handle('/taxonomy/search/<model>/<query>', 'plugins.taxonomy@search_terms', 'taxonomy@search_terms')

    # Admin sidebar menu
    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500)


__init()
