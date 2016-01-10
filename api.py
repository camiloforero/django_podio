# -*- coding: utf-8 -*-
from pypodio2 import api

from django.utils.html import strip_tags

class PodioApi:

    CLIENT_ID = "natco2015"
    CLIENT_SECRET = "6FHzzKdpWDz3UpBJzxRgaIHM88wqQZR6eIN2Q9v31UbdvqWvl9fnZL4Xo3xpROfy"

    app_id = None
    _client = None

    def __init__(self, app_id, app_token=None):
        self.app_id = app_id
        self._getClient(app_token)

    def _getClient(self, app_token=None):
        if app_token is None:
            from . import models
            app_token = models.Aplicacion.objects.get(app_id=self.app_id).app_token
        self._client = api.OAuthAppClient(self.CLIENT_ID, self.CLIENT_SECRET, self.app_id, app_token)

    def getAppInfo(self):
        data = self._client.Application.find(self.app_id)
        return data

    def getAllItems(self):
        data = self._client.Item.filter(
            int(self.app_id),{
                'limit': 400,
                #'filters':[{
                    #"key":"96943879", #En este pedazo se está filtrando sobre un campo, se quiere coger sólo a los 
                    #"values":[1],
                #}],
            },
        )["items"]
        fields = [self.makeDict(item) for item in data]
        return fields

    def getItem(self, itemID, no_html = False):
        data = self._client.Item.find(int(itemID))
        item = self.makeDict(data, no_html=no_html)
        return item

    def getRawItem(self, itemID):
        data = self._client.Item.find(int(itemID))
        return data 


    def makeDict(self, item, nested=False, no_html=False):
        dictionary = dict([ (field["external_id"], self.getFieldValue(field, nested, no_html)) for field in item["fields"] ])
        return {'item': item["item_id"], 'values':dictionary}

    def getFieldValue(self, field, nested=False, no_html=False):
        if field["type"] == "category":
            return field["values"][0]["value"]["text"]
        elif field["type"] == "image":
            return [field["values"][0]["value"]["mimetype"], field["values"][0]["value"]["file_id"]]
        elif field["type"] == "date":
            return field["values"][0]
        elif field["type"] == "app":
            itemID = field["values"][0]["value"]["item_id"]
            if nested:
                return itemID
            else:
                data = self._client.Item.find(int(itemID))
                item = self.makeDict(data, nested=True)
                return item
        elif field["type"] == "text":
            text = field["values"][0]["value"]
            if no_html and field["config"]["settings"]["format"] == 'html':
                text = strip_tags(text)
            return text 
        else:
            return field["values"][0]["value"]

    def updateItem(self, item, values):
        """Mini Wrapper sobre la API de PODIO"""
        print item
        print values
        message = self._client.Item.update(item, {'fields':values})
        print message
        return message



