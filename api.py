# -*- coding: utf-8 -*-
import json
from pypodio2 import api

from django.utils.html import strip_tags

class PodioApi(object):

    CLIENT_ID = "natco2015"
    CLIENT_SECRET = "6FHzzKdpWDz3UpBJzxRgaIHM88wqQZR6eIN2Q9v31UbdvqWvl9fnZL4Xo3xpROfy"


    def __init__(self, app_id, app_token=None):
        self.app_id = app_id
        self._client = self._getClient(app_token)

    def _getClient(self, app_token=None):
        """
        Gets a client item from pypodio, from the app_id given to the podioApi object when it was created. Optionally it receives an app_token; in that case it doesn't need to fetch it from the database
        """
        if app_token is None:
            from . import models
            app_token = models.Aplicacion.objects.get(app_id=self.app_id).app_token
        return api.OAuthAppClient(self.CLIENT_ID, self.CLIENT_SECRET, self.app_id, app_token)

    def getAppInfo(self):
        """
        Returns raw information of the api object's application
        """
        data = self._client.Application.find(self.app_id)
        return data

    def getAllItems(self):
        """
        Returns all items from the application of the api object
        """
        data = self._client.Item.filter(
            int(self.app_id), {
                'limit': 400,
#                'filters':[{
#                    "key":"96943879", #En este pedazo se está filtrando sobre un campo, se quiere coger sólo a los
#                    "values":[1],
#                }],
            },
        )["items"]
        fields = [self.makeDict(item) for item in data]
        return fields

    def getItem(self, itemID, no_html=False):
        """
        Returns a dictionary with a PODIO item's values
        """
        data = self._client.Item.find(int(itemID))
        item = self.makeDict(data, no_html=no_html)
        return item

    def getRawItem(self, itemID):
        """
        Returns the raw dictionary data of a PODIO API request for an item
        """
        data = self._client.Item.find(int(itemID))
        return data


    def makeDict(self, item, nested=False, no_html=False):
        """
        Creates a dictionary with the external_id of the item's fields ad keys, and their values as the dictionary values.
        """
        dictionary = dict([(field["external_id"], self.getFieldValue(field, nested, no_html)) for field in item["fields"]])
        return {'item': item["item_id"], 'values':dictionary}

    def getFieldValue(self, field, nested=False, no_html=False):
        """
        Gets the value of a field from its raw JSON data

        Params:
            nested: If there is a relationship field and nested is set to true, it will fetch that item's dictionary data from the PODIO api and use it as the value. If false, it will use the item_id value
            no_html: Defines whether HTML will be stripped or not
        """
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

    def appendFile(self, itemID, fileName, fileData):
        """
            Sube un archivo a PODIO, y lo asocia a un item específico como adjunto.

            fileData: Es un objeto de tipo 'file' de python, abierto en modo binario y con permisos de lectura.
        """
        print 'comienzo de appendFile'
        fileData.seek(0) #En caso que el lector del archivo abierto no esté al comienzo
        print 'siguiente del appendfile'
        message = self._client.Files.create(fileName, fileData)
        print 'mensaje 1'
        print message
        print 'printing message 2'
        print '%s, %s, %s' % (message['file_id'], 'item', itemID)
        self._client.Files.attach(message['file_id'], 'item', itemID)
        print 'acabó'
        print message2
        return message2


    def comment(self, commentable_type, commentable_id, attributes):
        attributes = json.dumps(attributes)
        return self._client.transport.POST(url="/comment/%s/%s/" % (commentable_type, commentable_id),
            body = attributes, type='application/json')


