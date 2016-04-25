# encoding=utf-8
from __future__ import unicode_literals

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
        item_key, field_key = key.split('#')
        newDict[value] = oldDict[int(item_key)]['value']['values'][int(field_key)]
    print newDict
    return newDict

def hyphen_to_underscore(oldDict):
    newDict = {}
    for key, value in oldDict.iteritems():
        newDict[key.replace('-', '_')] = value
    return newDict

def flatten_item(item):
    """
    This function transforms a complex item, as returned by the PODIO api, into a simpler, flat one
    """
    pass #not sure if it is even necessary
