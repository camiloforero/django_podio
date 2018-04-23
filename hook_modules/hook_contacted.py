# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb
from datetime import datetime

def run(appID, params, hook=None):
    p_api = api.PodioApi(appID)
    item = p_api.get_item(params['item_id'])
    stage = item['values'][151795769]['value']
    stage_number = int(stage.split(' - ')[0])
    if stage_number != 0 and 159724899 not in item['values']:
        p_api.updateItem(params['item_id'], {
            159724899: {'start_utc':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        })

    return 'success. item_id: %s, app_id: %s' % (params['item_id'], appID)
        
