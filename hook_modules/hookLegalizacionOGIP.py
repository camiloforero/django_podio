# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][122301101]['value'] == 'Si':
        transformer = [
            ('122301093#122297407', 114271376), #Nombre del trainee
            ('122301093#122297411', 114271380), #EP Id, o EXPA Code
            ('122301093#122297412', 114271381), #TN-ID
            (122301095, 114271385), #Cédula
            (122301096, 114271386), #Cédula escaneada
            (122301097, 114271387), #Fecha de inicio de la experiencia
            (122301098, 114271388), #Fecha de pago
            (122301099, 114271389), #Total pagado
            (122301100, 114271390), #FOto del recibo de pago
            (122301102, 114271396), #Autorizo a AIESEC en COlombia
        ]
        extra_data = {
            114271377:2, #Para colocar el programa de OGIP
            114271383:1  #Para que el comité local sea Andes
        }
            
        ans = podioApi.copy_item(params['item_id'], 14874570, transformer, extra_data)
        return ans
        
