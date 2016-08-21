# encoding:utf-8
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][126474412]['value'] == 'Aceptado como miembro de AIESEC' and item['values'][126474414]['value'] == 'Andes':
        transformer = [ #Primero el origen y después el destino
            (126474408, 117701584), #Nombre del trainee
            (126474409, 118634876), #Cedula
            (126474415, 117701824), #Email
            (126474410, 127294461), #Foto
            (126474416, 117701826), #Celular
            (126474419, 120001811), #Universidad
            (126474421, 127294462), #Semestre
            #(, ), #Pasaporte
            #(, ), #Pasaporte con estampado de la visa
            #(, ), #Seguro internacional
            #(, ), #Memodeal
        ]
        extra_data = {
            117759550:1, #Asignarlo como newbie
            117701833:3, #Rol de TMP
        }
            
        ans = podioApi.copy_item(params['item_id'], 15280717, transformer, extra_data)
        return ans
        
