"""Taxonomy Endpoints
"""
from pytsite import http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def search_terms(args: dict, inp: dict) -> _http.response.JSON:
    """Search taxonomy term titles
    """
    model = args.get('model')
    query = args.get('query')
    exclude = inp.get('exclude', [])

    if isinstance(exclude, str):
        exclude = [exclude]

    f = _api.find(model)

    if exclude:
        f.ninc('title', exclude)

    for word in query.split(' '):
        f.where('title', 'regex_i', word.strip())

    return _http.response.JSON([e.f_get('title') for e in f.get(10)])
