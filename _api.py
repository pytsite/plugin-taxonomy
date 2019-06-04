"""PytSite Taxonomy API Functions.
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from typing import Union, Optional
from pytsite import reg, router, lang, util
from plugins import admin, odm
from . import _error
from ._model import Term

_models = []


def register_model(model: str, cls, menu_title: str = None, menu_weight: int = 0, menu_icon: str = 'fa fas fa-tags',
                   menu_sid: str = 'taxonomy', menu_roles: Union[str, list, tuple] = ('admin', 'dev'),
                   menu_permissions: Union[str, list, tuple] = None):
    """Register a taxonomy model
    """
    if model in _models:
        raise RuntimeError("Taxonomy model '{}' is already registered".format(model))

    if isinstance(cls, str):
        cls = util.get_module_attr(cls)

    if not issubclass(cls, Term):
        raise TypeError('Subclass of {} expected'.format(Term))

    odm.register_model(model, cls)
    _models.append(model)

    if reg.get('env.type') == 'wsgi' and menu_title:
        menu_url = router.rule_path('odm_ui@admin_browse', {'model': model})
        admin.sidebar.add_menu(
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

    f = odm.find(model)

    if f.mock.has_field('weight'):
        f.sort([('weight', odm.I_DESC)])
    elif f.mock.has_field('order'):
        f.sort([('order', odm.I_ASC)])

    if not language:
        f.eq('language', lang.get_current())
    elif language != '*':
        f.eq('language', language)

    return f


def get(model: str, title: str = None, alias: str = None, language: str = None,
        exceptions: bool = False) -> Optional[Term]:
    """Find a term by title
    """
    if not (title or alias):
        raise ValueError('At least title or alias argument must be specified')

    f = find(model, language)
    if title:
        f.regex('title', '^{}$'.format(title), True)
    if alias:
        f.eq('alias', alias)

    term = f.first()

    if not term and exceptions:
        raise _error.TermNotExist(model, alias, language or lang.get_current())

    return term


def dispense(model: str, title: str, alias: str = None, language: str = None, parent: Term = None) -> Term:
    """Dispense a new term or raise exception if term with specified alias already exists
    """
    if alias and get(model, alias=alias, language=language):
        raise _error.TermExists(model, alias, language or lang.get_current())

    term = odm.dispense(model)  # type: Term
    term.title = title.strip()
    term.parent = parent
    if term.has_field('language'):
        term.language = language or lang.get_current()
    if term.has_field('alias') and alias:
        term.alias = alias or util.transform_str_2(title, language)

    return term


def sanitize_alias(model: str, s: str, language: str = None) -> str:
    """Sanitize an alias string
    """
    s = util.transform_str_2(s, language)

    itr = 0
    while True:
        if not find(model, language).eq('alias', s).count():
            return s

        itr += 1
        if itr == 1:
            s += '-1'
        else:
            s = re.sub('-\d+$', '-' + str(itr), s)
