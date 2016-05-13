# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID)
    item = podioApi.get_item(params['item_id'], external_id=False)
    #pdb.set_trace()

    return 'success. item_id: %s, app_id: %s' % (params['item_id'], appID)
