# encoding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.core.validators import validate_email

MESES = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
    ]


def dictSwitch(oldDict, transformer, related_transformer=None, ignore_unknown=False):
    """
    This method maps the keys of a dictionary to new keys, according to the key mapping present in the transformer dict. If a mapping is not found, it will keep the old key with it's value.
    If oldDict has a structure of {'old_key1': 'value1', ...} and transformer is {'old_key1':'new_key1', ...}, then this method will return {'new_key1', 'value1', ...} as the output.
    params:
        oldDict: A dictionary with the values and the old keys to be replaced
        transformer: A dictionary that maps the old keys with the new ones
        related_transformer: A dictionary that maps fields inside a related item to the new key values they should take
        ignore_unknown: Determines whether keys not present in the transformer will be added to the final dictionary, or simply ignored.
    """
    if related_transformer is None:
        related_transformer = {}
    newDict = {}
    for key, value in oldDict.iteritems():
        try:
            new_key = transformer[key]
            newDict[new_key] = value
        except KeyError:
            if not ignore_unknown:
                newDict[key] = value
    for key, value in related_transformer.iteritems():
        keys = key.split('#')
        if len(keys) == 2:
            newDict[value] = oldDict[int(keys[0])]['value']['values'][int(keys[1])]
        elif len(keys) == 3:
            newDict[value] = oldDict[int(keys[0])]['value']['values'][int(keys[1])]['value']['values'][int(keys[2])]
    #print newDict
    return newDict

def hyphen_to_underscore(oldDict):
    newDict = {}
    for key, value in oldDict.iteritems():
        newDict[key.replace('-', '_')] = value
    return newDict

def flatten_dict(dct):
    """
    This function transforms a complex item, as returned by the PODIO api, into a simpler, flat one
    It also converts raw dates into their spanish values
    """
    ans = {}
    for key, value in dct.iteritems():
        if value['type'] == 'date':
            date = datetime.strptime(value['value']['start_date'], "%Y-%m-%d")
            flat_date = date.strftime('%d de %%s, %Y') % MESES[int(date.strftime('%m')) - 1]
            ans[key] = flat_date
        else:
            ans[key] = value["value"]
    return ans  

def retrieve_email(value, item):
    try:
        validate_email(value)
        return value
    except:
        try:
            return item['values'][int(value)]['value']
        except ValueError:
            app_id, field_id = value.split("#")
            return item['values'][int(app_id)]['value']['values'][int(field_id)]['value']
