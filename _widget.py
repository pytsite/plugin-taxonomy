"""PytSite Taxonomy Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from pytsite import router, tpl
from plugins import widget, odm, odm_ui
from . import _api


class TermSelect(odm_ui.widget.EntitySelect):
    """Term Select
    """

    def __init__(self, uid: str, **kwargs):
        kwargs.setdefault('minimum_input_length', 1)
        kwargs.setdefault('sort_by', 'order')

        super().__init__(uid, **kwargs)


class TokensInput(widget.input.Tokens):
    """Term Tokens Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = []

        super().__init__(uid, **kwargs)

        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified')

        self._remote_source = router.rule_url('taxonomy@search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })

        self._data.update({
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        })

    def set_val(self, value, **kwargs):
        """Set value of the widget
        """
        if value is None:
            return super().set_val(value, **kwargs)

        if isinstance(value, str):
            value = value.split(',')

        clean_value = []
        for v in value:
            if isinstance(v, odm.model.Entity):
                clean_value.append(v)
            elif isinstance(v, str) and v:
                term = _api.get(self._model, v)
                if not term:
                    term = _api.dispense(self._model, v).save()
                clean_value.append(term)

        super().set_val(clean_value)

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget
        """
        html_input = htmler.Input(
            type='text',
            id=self._uid,
            name=self._name,
            value=','.join([v.f_get('title') for v in self.get_val()]),
            css=' '.join(('form-control', self._css)),
        )

        return html_input


class Cloud(widget.Abstract):
    """Terms Cloud Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')
        if not _api.is_model_registered(self._model):
            raise ValueError("'{}' is not a registered taxonomy model.".format(self._model))

        self._tpl = kwargs.get('tpl', 'taxonomy@widget/cloud')
        self._num = kwargs.get('num', 10)
        self._link_pattern = kwargs.get('link_pattern', '/{}/%s'.format(self._model))
        self._link_pattern_field = kwargs.get('link_pattern_field', 'alias')
        self._term_title_pattern = kwargs.get('term_title_pattern', '%s')
        self._term_css = kwargs.get('term_css', 'label label-default')
        self._title_tag = kwargs.get('title_tag', 'h3')
        self._css += ' widget-taxonomy-cloud widget-taxonomy-cloud-{}'.format(self._model)

    @property
    def model(self) -> str:
        return self._model

    @property
    def num(self) -> int:
        return self._num

    @property
    def link_pattern(self) -> str:
        return self._link_pattern

    @property
    def link_pattern_field(self) -> str:
        return self._link_pattern_field

    @property
    def term_title_pattern(self) -> str:
        return self._term_title_pattern

    @property
    def term_css(self) -> str:
        return self._term_css

    @property
    def title_tag(self) -> str:
        return self._title_tag

    @property
    def terms(self) -> list:
        return list(_api.find(self._model).get(self._num))

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget.
        :param **kwargs:
        """
        return htmler.TagLessElement(tpl.render(self._tpl, {'widget': self}))
