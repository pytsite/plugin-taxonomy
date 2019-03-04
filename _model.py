"""PytSite Taxonomy Plugin Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Tuple as _Tuple
from math import ceil as _ceil
from pytsite import lang as _lang, events as _events, routing as _routing
from plugins import widget as _widget, odm as _odm, file_storage_odm as _file_storage_odm, odm_ui as _odm_ui, \
    file as _file, form as _form, file_ui as _file_ui
from . import _widget as _t_widget


class Term(_odm_ui.model.UIEntity):
    """Taxonomy Term Model
    """

    def _setup_fields(self):
        """Hook
        """
        self.define_field(_odm.field.String('title', is_required=True))
        self.define_field(_odm.field.String('alias', is_required=True))
        self.define_field(_odm.field.String('language', is_required=True, default=_lang.get_current()))
        self.define_field(_odm.field.Integer('weight'))
        self.define_field(_odm.field.Integer('order'))
        self.define_field(_file_storage_odm.field.Image('image'))

    def _setup_indexes(self):
        """Hook
        """
        if self.has_field('title'):
            self.define_index([('title', _odm.I_TEXT)])

        if self.has_field('alias'):
            if self.has_field('language'):
                self.define_index([('alias', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)
            else:
                self.define_index([('alias', _odm.I_ASC)], unique=True)

        if self.has_field('weight'):
            if self.has_field('language'):
                self.define_index([('language', _odm.I_ASC), ('weight', _odm.I_DESC)])
            else:
                self.define_index([('weight', _odm.I_DESC)])

        if self.has_field('order'):
            if self.has_field('language'):
                self.define_index([('language', _odm.I_ASC), ('order', _odm.I_ASC)])
            else:
                self.define_index([('order', _odm.I_ASC)])

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'taxonomy'

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str, ...]:
        return 'create', 'modify', 'delete'

    @property
    def title(self) -> str:
        return self.f_get('title')

    @title.setter
    def title(self, value: str):
        self.f_set('title', value)

    @property
    def alias(self) -> str:
        return self.f_get('alias')

    @alias.setter
    def alias(self, value: str):
        self.f_set('alias', value)

    @property
    def language(self) -> str:
        return self.f_get('language')

    @language.setter
    def language(self, value: str):
        self.f_set('language', value)

    @property
    def weight(self) -> int:
        return self.f_get('weight')

    @weight.setter
    def weight(self, value: int):
        self.f_set('weight', value)

    @property
    def order(self) -> int:
        return self.f_get('order')

    @order.setter
    def order(self, value: int):
        self.f_set('order', value)

    @property
    def image(self) -> _file.model.AbstractImage:
        return self.f_get('image')

    @image.setter
    def image(self, value: _file.model.AbstractImage):
        self.f_set('image', value)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook
        """
        if field_name == 'alias':
            from . import _api

            if value is None:
                value = ''

            if not isinstance(value, str):
                raise RuntimeError('str or None expected')

            value = value.strip()
            if not self.is_new:
                # Sanitize CHANGED alias for EXISTING term
                term = _api.find(self.model).eq('alias', value).first()
                if not term or term != self:
                    value = _api.sanitize_alias(self.model, value, self.language)
            else:
                # Sanitize alias for NEW term
                value = _api.sanitize_alias(self.model, value, self.language)

        elif field_name == 'language':
            # Check if language code is correct
            if value not in _lang.langs():
                raise ValueError("Language '{}' is not supported".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        super()._on_pre_save(**kwargs)

        if self.has_field('alias') and not self.alias:
            self.f_set('alias', self.f_get('title'))

        if self.is_new and self.has_field('order') and not self.order:
            from . import _api
            e = _api.find(self.model).eq('_parent', self.parent).sort([('order', _odm.I_DESC)]).first()
            self.order = ((int(_ceil(e.order / 10.0)) * 10) + 10) if e else 10

        _events.fire('taxonomy@term.pre_save', term=self)

    def _on_pre_delete(self, **kwargs):
        """Hook
        """
        super()._on_pre_delete(**kwargs)

        _events.fire('taxonomy@term.pre_delete', term=self)

    def _on_after_delete(self, **kwargs):
        """Hook
        """
        # Delete attached image
        if self.has_field('image') and self.image:
            self.image.delete()

    def odm_ui_browser_setup(self, browser: _odm_ui.Browser):
        """Hook
        """
        data_fields = [
            ('title', 'taxonomy@title'),
        ]

        if self.has_field('alias'):
            data_fields.append(('alias', 'taxonomy@alias'))

        if self.has_field('weight'):
            data_fields.append(('weight', 'taxonomy@weight'))

        browser.data_fields = data_fields
        browser.default_sort_order = _odm.I_ASC

        if self.has_field('order'):
            browser.default_sort_field = 'order'
        elif self.has_field('weight'):
            browser.default_sort_field = 'weight'
        else:
            browser.default_sort_field = 'title'

    def odm_ui_browser_setup_finder(self, finder: _odm.SingleModelFinder, args: _routing.ControllerArgs):
        super().odm_ui_browser_setup_finder(finder, args)

        finder.eq('language', _lang.get_current())

    def odm_ui_browser_row(self) -> dict:
        """Hook
        """
        r = {
            'title': self.title,
        }

        if self.has_field('alias'):
            r['alias'] = self.alias

        if self.has_field('weight'):
            r['weight'] = self.weight

        return r

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook
        """
        # Parent
        frm.add_widget(_t_widget.TermSelect(
            uid='_parent',
            model=self.model,
            exclude=self if not self.is_new else None,
            exclude_descendants=True,
            label=self.t('parent'),
            append_none_item=not self.get_field('_parent').is_required,
            value=self.parent,
        ))

        # Title
        if self.has_field('title'):
            frm.add_widget(_widget.input.Text(
                uid='title',
                label=_lang.t('taxonomy@title'),
                value=self.title,
                required=self.get_field('title').is_required,
            ))

        # Alias
        if self.has_field('alias'):
            frm.add_widget(_widget.input.Text(
                uid='alias',
                label=_lang.t('taxonomy@alias'),
                value=self.f_get('alias'),
            ))

        # Weight
        if self.has_field('weight'):
            frm.add_widget(_widget.input.Integer(
                uid='weight',
                label=_lang.t('taxonomy@weight'),
                value=self.weight,
                h_size='col-sm-3 col-md-2 col-lg-1'
            ))

        # Image
        if self.has_field('image'):
            frm.add_widget(_file_ui.widget.ImagesUpload(
                uid='image',
                label=_lang.t('taxonomy@image'),
                required=self.get_field('image').is_required,
                value=self.image,
            ))

        # Language
        if self.has_field('language'):
            lng = _lang.get_current() if self.is_new else self.language
            frm.add_widget(_widget.static.Text(
                uid='language',
                label=_lang.t('taxonomy@language'),
                text=_lang.lang_title(lng),
                value=lng,
                hidden=len(_lang.langs()) == 1,
            ))

    def odm_ui_mass_action_entity_description(self) -> str:
        """Hook
        """
        return self.title

    def odm_ui_widget_select_search_entities(self, f: _odm.MultiModelFinder, args: dict):
        f.eq('language', args.get('language', _lang.get_current()))

        query = args.get('q')
        if query:
            f.regex('title', '{}'.format(query), True)

    def odm_ui_widget_select_search_entities_title(self, args: dict):
        return self.title

    def as_jsonable(self) -> dict:
        r = super().as_jsonable()

        if self.has_field('title'):
            r['title'] = self.title
        if self.has_field('alias'):
            r['alias'] = self.alias
        if self.has_field('weight'):
            r['weight'] = self.weight
        if self.has_field('order'):
            r['order'] = self.order
        if self.has_field('language'):
            r['language'] = self.language
        if self.has_field('image') and self.image:
            r['image'] = self.image.as_jsonable()

        return r
