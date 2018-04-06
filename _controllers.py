"""Taxonomy Endpoints
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, routing as _routing, http as _http
from . import _api


class SearchTerms(_routing.Controller):
    def exec(self):
        """Search taxonomy term titles
        """
        exclude = _router.request().inp.get('exclude', [])

        if isinstance(exclude, str):
            exclude = [exclude]

        f = _api.find(self.arg('model'))

        if exclude:
            f.ninc('title', exclude)

        for word in self.arg('query').split(' '):
            f.regex('title', word.strip(), True)

        return _http.response.JSON([e.f_get('title') for e in f.get(10)])
