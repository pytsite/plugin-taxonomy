"""PytSite Taxonomy API Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from typing import Union as _Union, Optional as _Optional
from pytsite import reg as _reg, router as _router, lang as _lang, util as _util
from plugins import admin as _admin, odm as _odm
from . import _error
from ._model import Term as _Term

_models = []


def register_model(model: str, cls, menu_title: str, menu_weight: int = 0, menu_icon: str = 'fa fa-tags',
                   menu_sid: str = 'settings', menu_roles: _Union[str, list, tuple] = ('admin', 'dev')):
    """Register a taxonomy model
    """
    if model in _models:
        raise RuntimeError("Model '{}' is already registered as taxonomy model".format(model))

    if isinstance(cls, str):
        cls = _util.get_module_attr(cls)

    if not issubclass(cls, _Term):
        raise TypeError('Subclass of {} expected'.format(_Term))

    _odm.register_model(model, cls)
    _models.append(model)

    if _reg.get('env.type') == 'wsgi':
        menu_url = _router.rule_path('odm_ui@browse', {'model': model})
        _admin.sidebar.add_menu(
            menu_sid, model, menu_title, menu_url, menu_icon,
            weight=menu_weight,
            roles=menu_roles,
            permissions=('odm_auth@create.' + model, 'odm_auth@modify.' + model, 'odm_auth@delete.' + model),
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
    return find(model, language).where('title', 'regex_i', '^{}$'.format(title)).first()


def find_by_alias(model: str, alias: str, language: str = None) -> _Optional[_Term]:
    """Find a term by alias
    """
    return find(model, language).eq('alias', alias).first()


def get(model: str, alias: str, language: str = None):
    """Get a term by alias
    """
    term = find_by_alias(model, alias, language)

    if not term:
        raise _error.TermNotExist(model, alias, language)

    return term


def dispense(model: str, title: str, alias: str = None, language: str = None, parent: _Term = None) -> _Term:
    """Create new term or dispense existing
    """
    try:
        term = get(model, alias, language)
    except _error.TermNotExist:
        term = _odm.dispense(model)  # type: _Term
        term.title = title.strip()
        term.parent = parent
        if term.has_field('language'):
            term.language = language or _lang.get_current()
        if term.has_field('alias') and alias:
            term.alias = alias or _util.transform_str_2(title)

    return term


def create(model: str, title: str, alias: str = None, language: str = None, parent: _Term = None) -> _Term:
    """Create a new term
    """
    if find_by_alias(model, alias, language):
        raise _error.TermExists(model, alias, language)

    return dispense(model, title, alias, language, parent)


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
