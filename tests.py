# coding=utf-8
from django.test import TestCase
from . import models, api
from pypodio2 import transport

import pdb

class CreateClientTest(TestCase):
    TEST_APP_ID = '14406445'
    TEST_APP_TOKEN = 'ff757f13949943d19eaa2b27cc475909'

    def test_create(self):
        testApi = api.PodioApi(self.TEST_APP_ID, self.TEST_APP_TOKEN)

    def test_create_wrong(self):
        with self.assertRaises(transport.TransportException):
            testApi = api.PodioApi(self.TEST_APP_ID, 'ndj29dlg90d4xk560d9dh49vhs4nfkv8')

    

class CreateAplicacionTest(TestCase):
    TEST_APP_ID = '14406445'
    TEST_APP_TOKEN = 'ff757f13949943d19eaa2b27cc475909'
    
    def test_create(self):
        testApp = models.Aplicacion(app_id=self.TEST_APP_ID, app_token=self.TEST_APP_TOKEN)
        testApp.save()

    def test_create_wrong(self):
        testApp = models.Aplicacion(app_id=self.TEST_APP_ID, app_token='hsjduenahsudheufhoe7f9ajshf8a8')
        with self.assertRaises(transport.TransportException):
            testApp.save()
        
class CreateHookTest(TestCase):    
    TEST_APP_ID = '14406445'
    TEST_APP_TOKEN = 'ff757f13949943d19eaa2b27cc475909'
    def test_create(self):
        testApp = models.Aplicacion(app_id=self.TEST_APP_ID, app_token=self.TEST_APP_TOKEN)
        testApp.save()
        testHook = models.Hook(name='testHook', application=testApp, module='testModule', trigger='item.create')
        testHook.save()
        #TODO: Check on the application whether this hook was actually created or not.
        #TODO: Check whether the hook has been verified
        #TODO: Check that the hook_id parameter has been set successfully

    def test_delete(self):
        pass
# Create your tests here.
