# coding=utf-8
from django.db import models
import inspect
import field_types

class Aplicacion(models.Model):
    """Esta clase representa una aplicación de PODIO. 
    """
    nombre = models.CharField(max_length=32, unique=True)
    app_id = models.CharField(max_length=8, primary_key=True)
    app_token = models.CharField(max_length=32, help_text=u"Escribe acá el token de la aplicación. Éste lo puedes encontrar en PODIO dentro de la parte de desarrolladores. Alternativamente, escribe tu token personal si quieres que las acciones que hace esta aplicación se hagan en tu nombre")
    link = models.URLField()
    def __unicode__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        if not self.nombre:
            from . import api
            api = api.PodioApi(self.app_id, self.app_token)
            data = api.getAppInfo()
            self.nombre = data['config']['name']
            self.link = data['url']
            super(Aplicacion, self).save(*args, **kwargs)
        else:
            super(Aplicacion, self).save(*args, **kwargs)
            
    class Meta:
        verbose_name_plural = "aplicaciones"

class Campo(models.Model):
    """Representa un campo dentro de una aplicación de PODIO.
    """

    nombre = models.CharField(max_length=32)
    id = models.CharField(max_length=16, primary_key=True)
    external_id=models.CharField(max_length=32)
    #tipo = models.CharField(max_length=4, choices=inspect.getmembers(field_types, inspect.isclass)

class Hook(models.Model):
    HOOK_TYPES = (
        ('item.create', 'item.create'),
        ('item.update', 'item.update'),
        ('item.delete', 'item.delete'),
    )
    name = models.CharField(max_length=32, primary_key=True)
    application = models.ForeignKey(Aplicacion, on_delete=models.CASCADE)
    module = models.CharField(max_length=32)
    trigger = models.CharField(max_length=16, choices=HOOK_TYPES)
    hook_id = models.CharField(max_length=32)
    def save(self, *args, **kwargs):
        from . import api
        api = api.PodioApi(self.application_id)
        url = 'http://104.131.143.133/app/podio/hooks/%s/' % self.name
        attributes = {'url': url, 'type': self.trigger}
        response = api._client.Hook.create('app', self.application_id, attributes) 
        hook_id = response['hook_id']
        super(Hook, self).save(*args, **kwargs)


    


# Create your models here.
