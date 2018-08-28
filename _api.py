"""PytSite Taxonomy API Functions.
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from typing import Union as _Union, Optional as _Optional
from pytsite import reg as _reg, router as _router, lang as _lang, util as _util
from plugins import admin as _admin, odm as _odm
from . import _error
from ._model import Term as _Term

_models = []


def register_model(model: str, cls, menu_title: str, menu_weight: int = 0, menu_icon: str = 'fa fas fa-tags',
                   menu_sid: str = 'taxonomy', menu_roles: _Union[str, list, tuple] = ('admin', 'dev'),
                   menu_permissions: _Union[str, list, tuple] = None):
    """Register a taxonomy model
    """
    if model in _models:
        raise RuntimeError("Taxonomy model '{}' is already registered".format(model))

    if isinstance(cls, str):
        cls = _util.get_module_attr(cls)

    if not issubclass(cls, _Term):
        raise TypeError('Subclass of {} expected'.format(_Term))

    _odm.register_model(model, cls)
    _models.append(model)

    if _reg.get('env.type') == 'wsgi':
        menu_url = _router.rule_path('odm_ui@admin_browse', {'model': model})
        _admin.sidebar.add_menu(
            menu_sid, model, menu_title, menu_url, menu_icon,
            weight=menu_weight,
            roles=menu_roles,
            permissions=menu_permissions,
        )


def is_model_registered(model: str) -> bool:
    """Check if the model is registered as taxonomy model
    """
    return model in _models


def find(model: str, language: str = None):
    """Get finder for the taxonomy model
    """
    if not is_model_registered(model):
        raise RuntimeError("Model '{}' is not registered as taxonomy model.".format(model))

    f = _odm.find(model)

    if f.mock.has_field('weight'):
        f.sort([('weight', _odm.I_DESC)])
    elif f.mock.has_field('order'):
        f.sort([('order', _odm.I_ASC)])

    if not language:
        f.eq('language', _lang.get_current())
    elif language != '*':
        f.eq('language', language)

    return f


def find_by_title(model: str, title: str, language: str = None) -> _Optional[_Term]:
    """Find a term by title
    """
    return find(model, language).regex('title', '^{}$'.format(title), True).first()


def find_by_alias(model: str, alias: str, language: str = None) -> _Optional[_Term]:
    """Find a term by alias
    """
    return find(model, language).eq('alias', alias).first()


def get(model: str, alias: str, language: str = None):
    """Get a term by alias, raise exception if not it does not exist
    """
    term = find_by_alias(model, alias, language)

    if not term:
        raise _error.TermNotExist(model, alias, language or _lang.get_current())

    return term


def dispense(model: str, title: str, alias: str = None, language: str = None, parent: _Term = None) -> _Term:
    """Dispense a new term or raise exception if term with specified alias already exists
    """
    if alias and find_by_alias(model, alias, language):
        raise _error.TermExists(model, alias, language or _lang.get_current())

    term = _odm.dispense(model)  # type: _Term
    term.title = title.strip()
    term.parent = parent
    if term.has_field('language'):
        term.language = language or _lang.get_current()
    if term.has_field('alias') and alias:
        term.alias = alias or _util.transform_str_2(title)

    return term


def sanitize_alias(model: str, s: str, language: str = None) -> str:
    """Sanitize an alias string
    """
    s = _util.transform_str_2(s)

    itr = 0
    while True:
        if not find(model, language).eq('alias', s).count():
            return s

        itr += 1
        if itr == 1:
            s += '-1'
        else:
            s = re.sub('-\d+$', '-' + str(itr), s)
