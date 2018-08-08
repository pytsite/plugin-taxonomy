"""PytSite Taxonomy Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ModelNotRegistered(Exception):
    def __init__(self, model: str):
        self._model = model

    def __str__(self) -> str:
        return "Taxonomy model '{}' is not registered".format(self._model)


class TermNotExist(Exception):
    def __init__(self, model: str, alias: str, language: str):
        self._model = model
        self._alias = alias
        self._language = language

    def __str__(self) -> str:
        return 'Term {}.{} [{}] is not exists'.format(self._model, self._alias, self._language)


class TermExists(Exception):
    def __init__(self, model: str, alias: str, language: str):
        self._model = model
        self._alias = alias
        self._language = language

    def __str__(self) -> str:
        return 'Term {}.{} [{}] already exists'.format(self._model, self._alias, self._language)
