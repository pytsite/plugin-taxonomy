"""PytSite Taxonomy Plugin Models
"""
from typing import Tuple as _Tuple
from pytsite import odm_ui as _odm_ui, lang as _lang, odm as _odm, widget as _widget, form as _form, \
    events as _events, file as _file, file_storage_odm as _file_storage_odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Term(_odm_ui.model.UIEntity):
    """Taxonomy Term Model
    """

    def _setup_fields(self):
        """Hook
        """
        self.define_field(_odm.field.String('title', required=True, strip_html=True))
        self.define_field(_odm.field.String('alias', required=True, strip_html=True))
        self.define_field(_odm.field.String('language', required=True, default=_lang.get_current()))
        self.define_field(_odm.field.Integer('weight'))
        self.define_field(_odm.field.Integer('order'))
        self.define_field(_file_storage_odm.field.Image('image'))

    def _setup_indexes(self):
        """Hook
        """
        self.define_index([('alias', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)
        self.define_index([('language', _odm.I_ASC), ('weight', _odm.I_DESC)])
        self.define_index([('weight', _odm.I_ASC)])
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

    @property
    def alias(self) -> str:
        return self.f_get('alias')

    @property
    def language(self) -> str:
        return self.f_get('language')

    @property
    def weight(self) -> int:
        return self.f_get('weight')

    @property
    def order(self) -> int:
        return self.f_get('order')

    @property
    def image(self) -> _file.model.AbstractImage:
        return self.f_get('image')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook
        """
        if field_name == 'alias':
            from . import _api

            if value is None:
                value = ''

            if not isinstance(value, str):
                raise RuntimeError('str or None expected.')

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
                raise ValueError("Language '{}' is not supported.".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self, **kwargs):
        """Hook
        """
        super()._pre_save(**kwargs)

        # Alias is mandatory
        if not self.f_get('alias'):
            self.f_set('alias', self.f_get('title'))

        _events.fire('taxonomy.term.pre_save', term=self)

    def _pre_delete(self, **kwargs):
        """Hook
        """
        super()._pre_delete(**kwargs)

        _events.fire('taxonomy.term.pre_delete', term=self)

    def _after_delete(self, **kwargs):
        """Hook
        """
        # Delete attached image
        if self.has_field('image') and self.image:
            self.image.delete()

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        """Hook
        """
        data_fields = [
            ('title', 'taxonomy@title'),
            ('alias', 'taxonomy@alias'),
            ('weight', 'taxonomy@weight'),
            ('order', 'taxonomy@order'),
        ]

        browser.data_fields = data_fields
        browser.default_sort_field = 'order'
        browser.default_sort_order = _odm.I_ASC
        browser.finder_adjust = lambda finder: finder.eq('language', _lang.get_current())

    def odm_ui_browser_row(self) -> tuple:
        """Hook
        """
        return self.title, self.alias, self.weight, self.order

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook
        """
        # Title
        if self.has_field('title'):
            frm.add_widget(_widget.input.Text(
                weight=10,
                uid='title',
                label=_lang.t('taxonomy@title'),
                value=self.title,
                required=self.get_field('title').required,
            ))

        # Alias
        if self.has_field('alias'):
            frm.add_widget(_widget.input.Text(
                weight=20,
                uid='alias',
                label=_lang.t('taxonomy@alias'),
                value=self.f_get('alias'),
            ))

        # Weight
        if self.has_field('weight'):
            frm.add_widget(_widget.input.Integer(
                weight=30,
                uid='weight',
                label=_lang.t('taxonomy@weight'),
                value=self.weight,
                h_size='col-sm-3 col-md-2 col-lg-1'
            ))

        # Order
        if self.has_field('order'):
            frm.add_widget(_widget.input.Integer(
                weight=40,
                uid='order',
                label=_lang.t('taxonomy@order'),
                value=self.order,
                h_size='col-sm-3 col-md-2 col-lg-1',
                allow_minus=True
            ))

        # Image
        if self.has_field('image'):
            frm.add_widget(_file.widget.ImagesUpload(
                uid='image',
                weight=50,
                label=_lang.t('taxonomy@image'),
                required=self.get_field('image').required,
                value=self.image,
            ))

        # Language
        if self.has_field('language'):
            lng = _lang.get_current() if self.is_new else self.language
            frm.add_widget(_widget.static.Text(
                uid='language',
                weight=60,
                label=_lang.t('taxonomy@language'),
                title=_lang.lang_title(lng),
                value=lng,
            ))

    def odm_ui_mass_action_entity_description(self) -> str:
        """Hook
        """
        return self.title
