"""PytSite Taxonomy API Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from typing import Union as _Union
from pytsite import reg as _reg, router as _router, lang as _lang, util as _util
from plugins import admin as _admin, odm as _odm
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
    """Check if the model is registered as taxonomy model.
    """
    return model in _models


def find(model: str, language: str = None):
    """Get finder for the taxonomy model.
    """
    if not is_model_registered(model):
        raise RuntimeError("Model '{}' is not registered as taxonomy model.".format(model))

    f = _odm.find(model).sort([('weight', _odm.I_DESC)])

    if not language:
        f.eq('language', _lang.get_current())
    elif language != '*':
        f.eq('language', language)

    return f


def find_by_title(model: str, title: str, language: str = None) -> _Term:
    """Find term by title.
    """
    return find(model, language).where('title', 'regex_i', '^{}$'.format(title)).first()


def find_by_alias(model: str, alias: str, language: str = None) -> _Term:
    """Find term by alias.
    """
    return find(model, language).eq('alias', alias).first()


def dispense(model: str, title: str, alias: str = None, language: str = None) -> _Term:
    """Create new term or dispense existing.
    """
    if not is_model_registered(model):
        raise RuntimeError("Model '{}' is not registered as taxonomy model.".format(model))

    title = title.strip()

    if not alias:
        alias = _util.transform_str_2(title)

    # Trying to find term by title
    term = find(model, language).where('title', 'regex_i', '^' + title + '$').first()

    # If term is not found, trying to find it by alias
    if not term:
        term = find(model, language).eq('alias', alias).first()

    # If term is not found, create it
    if not term:
        term = _odm.dispense(model)
        term.f_set('title', title).f_set('language', language or _lang.get_current())
        if alias:
            term.f_set('alias', alias)

    return term


def sanitize_alias(model: str, s: str, language: str = None) -> str:
    """Sanitize an alias string.
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
