# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from . import settings
import inspect
import field_types

class Aplicacion(models.Model):
    """Esta clase representa una aplicación de PODIO. 
    """
    nombre = models.CharField(max_length=128, unique=True)
    workspace = models.CharField(help_text="Espacio de trabajo al cual pertenece esta aplicación", max_length=32)
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
            self.nombre = data['config']['name'] + ' - ' + self.workspace#TODO: Agregar el nombre del espacio de trabajo en el que se encuentra la aplicación
            self.link = data['url']
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
    name = models.CharField(help_text="The last parameter of the url this hook will have. FOr example, co.aiesec.org/podio/hooks/*name*", max_length=32, primary_key=True)
    label = models.CharField(help_text="A human readable name", max_length=64)
    application = models.ForeignKey(Aplicacion, on_delete=models.CASCADE)
    field = models.CharField(help_text="If empty, this will be an app hook. If not, it will be an app_field hook. One main difference is that with an item.update trigger, the frist one will be triggered every time anything is modified, while the second will trigger only when the specific field is modificed", max_length=16, null=True, blank=True)
    module = models.CharField(help_text="The name of the module, within the hook_modules filder, that will be run when this hook triggers", max_length=32)
    trigger = models.CharField(max_length=16, choices=HOOK_TYPES)
    hook_id = models.CharField(max_length=32)
    hook_url = models.CharField(max_length=128)
    uses = models.PositiveIntegerField(help_text="Número de veces que ha sido usado este hook", default=0, blank=True)
    def __unicode__(self):
        return self.label
    def clean(self, *args, **kwargs):
        from . import hooks
        try:
            hooks.HookDispatcher(self.label, self.module)
            super(Hook, self).clean(*args, **kwargs)
        except AttributeError as e:
            raise ValidationError({'module':"%s" % e})
    def save(self, *args, **kwargs):
        try:
            Hook.objects.get(pk=self.name)
        except Hook.DoesNotExist:
            from . import api
            api = api.PodioApi(self.application_id)
            self.hook_url = '%s/%s/%s/' % (settings.DOMAIN, settings.HOOK_URL, self.name)
            attributes = {'url': self.hook_url, 'type': self.trigger}
            if self.field is not None and self.field is not "":
                ref_type = 'app_field'
                ref_id = self.field
            else:
                ref_type = 'app'
                ref_id = self.application_id
            response = api._client.Hook.create(ref_type, ref_id, attributes) 
            self.hook_id = response['hook_id']
            super(Hook, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        from . import api
        api = api.PodioApi(self.application_id)
        api._client.Hook.delete(self.hook_id)
        super(Hook, self).delete(*args, **kwargs)


    


# Create your models here.
