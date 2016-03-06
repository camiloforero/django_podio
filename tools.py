# encoding=utf-8
from __future__ import unicode_literals

def dictSwitch(oldDict, transformer):
    newDict = {}
    for key, value in oldDict.iteritems():
        try:
            newDict[transformer[key]] = value
        except KeyError:
            newDict[key] = value
    return newDict

def hyphen_to_underscore(oldDict):
    newDict = {}
    for key, value in oldDict.iteritems():
        newDict[key.replace('-', '_')] = value
    return newDict
