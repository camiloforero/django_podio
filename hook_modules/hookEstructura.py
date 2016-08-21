# encoding:utf-8
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][125763518]['value'] == 'Aceptado como miembro de AIESEC' and item['values'][125763520]['value'] == 'Andes':
        transformer = [ #Primero el origen y después el destino
            (125763514, 117701584), #Nombre del trainee
            (125763515, 118634876), #Cedula
            (125763521, 117701824), #Email
            (125763516, 127294461), #Foto
            (125763522, 117701826), #Celular
            (125763525, 120001811), #Universidad
            (125763527, 127294462), #Semestre
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
        
