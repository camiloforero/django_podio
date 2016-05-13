from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .api import PodioApi
from . import hooks
from . import models

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
        hook = models.Hook.objects.get(pk=kwargs['hookName'])
        dispatcher = hooks.HookDispatcher(kwargs['hookName'], hook.module)
        dispatcher.test()
        return HttpResponse('success %s' % kwargs['hookName'])
    def post(self, request, *args, **kwargs):
        hook = models.Hook.objects.get(pk=kwargs['hookName'])
        dispatcher = hooks.HookDispatcher(kwargs['hookName'], hook.module)
        params = request.POST
        if params['type'] == 'hook.verify':
            api = PodioApi(hook.application_id)
            api._client.Hook.validate(params['hook_id'], params['code'])
            return HttpResponse('success') #TODO modificar
        else:
            dispatcher.module.run(hook.application_id, params, hook)
            hook.uses = hook.uses + 1
            hook.save()
            return HttpResponse('success') #TODO modificar
        

# Create your views here.
