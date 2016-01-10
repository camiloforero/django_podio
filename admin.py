# coding=utf-8
from django.contrib import admin
from .models import Aplicacion, Hook

@admin.register(Aplicacion)
class AplicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'app_id', 'link')
    readonly_fields = ('nombre', 'link')

@admin.register(Hook)
class HookAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'trigger', 'module')
    readonly_fields = ('hook_id', )

# Register your models here.
