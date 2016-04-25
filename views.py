from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .api import PodioApi
from . import hooks
from . import models

import logging

def ver_aplicacion(request, appID):
    api = PodioApi(appID)
    return HttpResponse(api.getAppInfo())

def ver_items(request, appID):
    api = PodioApi(appID)
    return HttpResponse(api.getAllItems())

def ver_item(request, appID, itemID):
    api = PodioApi(appID)
    return HttpResponse(api.getRawItem(itemID))

class HookView(View):
    def get(self, request, *args, **kwargs):
        hook = models.Hook.objects.get(name=kwargs['hookName'])
        dispatcher = hooks.HookDispatcher(kwargs['hookName'], hook.module)
        logger = logging.getLogger('django')
        logger.debug(kwargs)
        logger.debug('success')
        dispatcher.test()
        return HttpResponse('success %s' % kwargs['hookName'])
    def post(self, request, *args, **kwargs):
        hook = models.Hook.objects.get(name=kwargs['hookName'])
        dispatcher = hooks.HookDispatcher(kwargs['hookName'], hook.module)
        logger = logging.getLogger('django')
        params = request.POST
        if params['type'] == 'hook.verify':
            logger.debug('entro al verify')
            api = PodioApi(hook.application_id)
            api._client.Hook.validate(params['hook_id'], params['code'])
            return HttpResponse('success') #TODO modificar
        else:
            logger.debug(kwargs)
            logger.debug(params)
            dispatcher.module.run(hook.application_id, params, hook)
            hook.uses = hook.uses + 1
            hook.save()
            return HttpResponse('success') #TODO modificar
        

# Create your views here.
