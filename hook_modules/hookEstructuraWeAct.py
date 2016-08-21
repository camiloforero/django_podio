# encoding:utf-8
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][112443321]['value'] == 'Aceptado como miembro de AIESEC' and item['values'][112443323]['value'] == 'Andes':
        transformer = [ #Primero el origen y después el destino
            (112443317, 117701584), #Nombre del trainee
            (112443318, 118634876), #Cedula
            (112443324, 117701824), #Email
            (112443319, 127294461), #Foto
            (112443325, 117701826), #Celular
            (112443328, 120001811), #Universidad
            (112443330, 127294462), #Semestre
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
        
