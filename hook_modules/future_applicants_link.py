# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID)
    item = podioApi.get_item(params['item_id'], external_id=False)
    email = item['values'][102329869]['value']
    a = podioApi.find_referenceable_items(121611822, text=email)
    if len(a) > 0:
        podioApi.updateItem(params['item_id'], {121611822:int(a[0]['item_id'])}) 
    #pdb.set_trace()

    return 'success. item_id: %s, app_id: %s' % (params['item_id'], appID)
