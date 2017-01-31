# encoding:utf-8
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][122927930]['value']['values'][122923596]['value'] == 'GV' and item['values'][132671269]['value'] == 'Si':
        transformer = [
            ("122927930#122923594", 113794808), #Nombre del trainee
            ("122927930#122923598", 113794809), #Email
            ("122927930#122923597", 113794810), #EP Id, o EXPA Code
            ("122927930#122923600", 113794811), #TN-ID
            (122927945, 113796635), #Fecha de llegada a Colombia
            (122927946, 113794814), #Fecha de realización
            (122927947, 113794815), #Fecha de finalización
            (122927935, 113794816), #FOto de pasaporte
            (135327307, 113794817), #Foto del pasaporte con estampado de la visa (PIP)
            (122927942, 113794818), #Seguro internacional
            (122927950, 113794819), #Memodeal
        ]
        extra_data = {
            113794813:1, #TODO es un campo de categoría, probablemente LC
            113796330:1 #TODO qué es esto? Es un campo de categoría, pero no sabría cual
        }
            
        ans = podioApi.copy_item(params['item_id'], 14817777, transformer, extra_data)
        print ans
        return ans
        
