"""Taxonomy Endpoints
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router, routing, http
from . import _api


class SearchTerms(routing.Controller):
    def exec(self):
        """Search taxonomy term titles
        """
        exclude = router.request().inp.get('exclude', [])

        if isinstance(exclude, str):
            exclude = [exclude]

        f = _api.find(self.arg('model'))

        if exclude:
            f.ninc('title', exclude)

        for word in self.arg('query').split(' '):
            f.regex('title', word.strip(), True)

        return http.JSONResponse([e.f_get('title') for e in f.get(10)])
