# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pprint
from bs4 import BeautifulSoup
from pypodio2 import api
from . import settings

from django.utils.html import strip_tags

class PodioApi(object):

    def __init__(self, app_id, app_token=None, client=False):
        self.app_id = app_id
        self.client = client
        if client:
            self._client = self._get_user_client()
        else:
            self._client = self._getClient(app_token)

    def _getClient(self, app_token=None):
        """
        Gets a client item from pypodio, from the app_id given to the podioApi object when it was created. Optionally it receives an app_token; in that case it doesn't need to fetch it from the database
        """
        if app_token is None:
            from . import models
            app_token = models.Aplicacion.objects.get(app_id=self.app_id).app_token
        return api.OAuthAppClient(settings.CLIENT_ID, settings.CLIENT_SECRET, self.app_id, app_token)

    def _get_user_client(self):
        """
        Gets a client item from pypodio, from the app_id given to the podioApi object when it was created. Optionally it receives an app_token; in that case it doesn't need to fetch it from the database
        """
        return api.OAuthClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.USER, settings.PASSWORD)

    def getAppInfo(self):
        """
        Returns raw information of the api object's application, as a Python dictionary.
        """
        data = self._client.Application.find(self.app_id)
        return data

    def getAllItems(self):
        """
        Returns up to 500 items from the application of the api object
        """
        data = self._client.Item.filter(
            int(self.app_id), {
                'limit': 500,
#                'filters':[{
#                    "key":"96943879", #En este pedazo se está filtrando sobre un campo, se quiere coger sólo a los
#                    "values":[1],
#                }],
            },
        )["items"]
        fields = [self.makeDict(item) for item in data]
        return fields

    def get_filtered_items(self, filters, depth=1):
        """
        Returns items filtered according to certain parameters. See the PODIO API for more information on a filter syntax. TODO: how does this syntax exactly work?
        params:
        filters: a list of all the filters that will be applied
        """
        data = self._client.Item.filter(
            int(self.app_id), {
                'limit': 500,
                'filters':filters,
            },
        )["items"]
        fields = [self.make_dict(item, external_id=False, depth=depth) for item in data]
        return fields

    def get_items_by_view(self, view_id):
        """
        Returns all items belonging to a certain view, given by its ID. As all new methods, it automatically asks for the external ID
        params: 
        filters: a list of all the filters that will be applied
        """
        data = self.filter_by_view(
            int(self.app_id), int(view_id),{
                'limit': 400,
            },
        )["items"]
        fields = [self.make_dict(item, external_id=False) for item in data]
        return fields

    def getItem(self, itemID, no_html=False):
        """
        Returns a dictionary with a PODIO item's values
        """
        data = self._client.Item.find(int(itemID))
        item = self.makeDict(data, no_html=no_html)
        return item

    def get_item(self, itemID, no_html=False, external_id=True, depth=1, version=1):
        """
        Returns a dictionary with a PODIO item's type, and all its values
        itemID: The unique PODIO Item ID of the item that needs to be retrieved
        no_html: If true, all html code will either be deleted or converted to ODT format
        external_id: Whether the external_id or the field_id will be used as keys for the item values
        depth: How deep will the request go down the rabbit hole following related items and retrieving their values
        version: does nothing at the moment
        """
        data = self._client.Item.find(int(itemID))
        item = self.make_dict(data, no_html=no_html, external_id=external_id, depth=depth, version=version)
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

    def make_dict(self, item, external_id=True, no_html=False, depth=1, version='v1'):
        """
        Creates a dictionary with the external_id of the item's fields ad keys, and their values as the dictionary values. This second versions allows to choose between the field_id or the external_id for the dictionary's key, and adds the field type to the generated dictionary.
        Params:
            item: The item that is being retrieved
            depth: the number of levels that related apps will be followed
        """
        if external_id:
            key_type = "external_id"
        else:
            key_type = "field_id"

        dictionary = dict([(field[key_type], {"type": field["type"], "value": self.getFieldValue(field, no_html, external_id=external_id, depth=depth)}) for field in item["fields"]])
        return {'item': item["item_id"], 'values':dictionary}

    def getFieldValue(self, field, no_html=False, external_id=True, depth=1):
        """
        Gets the value of a field from its raw JSON data

        Params:
            depth: If there is a relationship field and depth has a value greater than zero, it will fetch that item's dictionary data from the PODIO api and use it as the value. If false, it will use the item_id value
            no_html: Defines whether HTML will be stripped or not
        """
        if field["type"] == "category":
            if field["config"]["settings"]["multiple"]:
                values = []
                for category in field["values"]:
                    values.append(category["value"]["text"])
                return values
            else:
                return field["values"][0]["value"]["text"]
        elif field["type"] == "image":
            values = []
            for image in field['values']:
                values.append([image["value"]["mimetype"], image["value"]["file_id"]])
            return values
        elif field["type"] == "date":
            return field["values"][0]
        elif field["type"] == "app":
            itemID = field["values"][0]["value"]["item_id"]
            if depth<=0:
                return itemID
            else:
                data = self._client.Item.find(int(itemID))
                if not external_id:
                    item = self.make_dict(data, external_id=external_id, depth=depth-1)
                else:
                    item = self.makeDict(data, nested=True)
                return item
        elif field["type"] == "text":
            text = field["values"][0]["value"]
            if no_html and field["config"]["settings"]["format"] == 'html':
                print text.encode('utf-8')
                html_text = BeautifulSoup(text, "html5lib")
                for p_tag in html_text.find_all('p'):
                    p_tag.unwrap()
                print html_text
                for br_tag in html_text.find_all('br'):
                    br_tag.name="text:line-break"
                html_text.find('html').unwrap()
                html_text.find('head').unwrap()
                html_text.find('body').unwrap()
                text = unicode(html_text)
                print text.encode('ascii', 'ignore')
                #text = strip_tags(text)
            return text
        elif field["type"] == "embed":
            return field["values"][0]["embed"]["url"]
        else:
            #print field["type"]
            return field["values"][0]["value"]

    def updateItem(self, item, values):
        """Mini Wrapper sobre la API de PODIO"""
        print 'Updating item: ' + unicode(item)
        item = int(item) #Importante: Para evitar que se caiga la api de PODIO más adelante
        message = self._client.Item.update(item, {'fields':values})
        return message

    def uploadFile(self, fileName, fileData):
        """
        Sube un archivo a PODIO, para que luego sea asociado a aquello que lo requiera
        fileName: El nombre que tendrá el archivo
        fileData: un file de Python

        Returns: the dictionary returned by pypodio. It has a key, "file_id", where the ID of the newly uploaded file can be found.
            

        """
        print "Attempting to upload file..."
        fileData.seek(0) #En caso que el lector del archivo abierto no esté al comienzo
        return self._client.Files.create(fileName, fileData)

    def appendFile(self, itemID, fileName, fileData):
        """
            Sube un archivo a PODIO, y lo asocia a un item específico como adjunto.

            fileData: Es un objeto de tipo 'file' de python, abierto en modo binario y con permisos de lectura.
        """
        itemID = int(itemID)
        message = self.uploadFile(fileName, fileData)
        print 'File upload completed successfully'
        print '%s, %s, %s' % (message['file_id'], 'item', itemID)
        message2 = self._client.Files.attach(message['file_id'], 'item', itemID)
        print message2
        return message2

    def copy_file(self, file_id):
        """
        Creates a copy of a file
        Params:
            file_id: the file to be copied. The current user or application must have permission to access it
        Returns: A dictionary. Its key, "file_id", contains the new id of the new, copied file.
        """
        return self._client.Files.copy(file_id)
        

    def create_item(self, attributes, app_id = None, silent=False, hook=True):
        if app_id is None:
            app_id = self.app_id
        return self._client.Item.create(app_id, attributes, silent, hook)

    def copy_item(self, origin_item_id, target_app_id, field_conversor, extra_data = None, silent=False, hook=True):
        """
        This method takes an item's values and copies them to a new item in the target app.
        Parameters:
            origin_item_id: The item_id of the original item from which the values will be taken
            target_app_id: The app_id of the application on which the new item will be created
            field_conversor: A tuple that pairs together the (field_id)s from the origin application to the destination application.
            extra_data: Represents data that is not present in the origin application but that should be added to the destination application, such as category fields, or default names. They can be always the same, or they can be guessed somehow from the existing fields
        """
        source_item = self.get_item(origin_item_id, external_id=False)
        if extra_data is None:
            destination_dict = {}
        else:
            destination_dict = extra_data
        try:
            for origin, destination in field_conversor:
                try:
                    origin = int(origin)
                    source_field = source_item["values"][origin]
                except ValueError:
                    related_id, field_id = origin.split('#')
                    source_field = source_item["values"][int(related_id)]["value"]["values"][int(field_id)]
                if source_field['type'] == "image":
                    new_value = []
                    for value in source_field['value']:
                        new_value.append(self.copy_file(value[1])['file_id'])
                else:
                    new_value = source_field['value']
                destination_dict[destination] = new_value
        except KeyError as e:
            self.comment(
                'item', 
                origin_item_id,
                {'value': 'Ha habido un error con la llave %s (IM lo sabe interpretar :)  ) pero probablemente no están todos los campos que pide la aplicación nacional y por eso no se pudo crear.' % str(e)}
            )
            return 'Key Error: ' + str(e)
        new_item = self.create_item({"fields":destination_dict}, app_id = target_app_id)
        self.comment(
            'item', 
            origin_item_id,
            {'value': 'Se ha copiado el EP al espacio nuevo de PODIO exitosamente en la direccion %s' % new_item['link']}
        )
        return new_item
        #make new item
        #return return code

############PODIO API Originals##############
#These methods are here because there is no equivalent in the official PODIO API. They follow the same style, and eventually they will be added to the official branch with a pull request.

    def find_referenceable_items(self, field_id, **kwargs):
        """
        Used to find possible items for a given application field.It searches the relevant apps for items matching the given text
        """
        return self._client.transport.GET(url="/item/field/%s/find" % field_id, **kwargs)

    def comment(self, commentable_type, commentable_id, attributes):
        """
        Comments an item. This one is made to be similar to the methods in the official API, but as they don't have a comment Area it is here instead
        """
        attributes = json.dumps(attributes)
        return self._client.transport.POST(url="/comment/%s/%s/" % (commentable_type, commentable_id),
            body = attributes, type='application/json')

    def filter_by_view(self, app_id, view_id, attributes, **kwargs):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self._client.transport.POST(url="/item/app/%d/filter/%d/" % (app_id, view_id), body=attributes, type="application/json", **kwargs)
