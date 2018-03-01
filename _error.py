"""PytSite Taxonomy Plugin Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TermExists(Exception):
    def __init__(self, model: str, alias: str):
        self._model = model
        self._alias = alias

    def __str__(self) -> str:
        return 'Term {}.{} already exists'.format(self._model, self._alias)
