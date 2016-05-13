# coding=utf-8
from django.contrib import admin
from .models import Aplicacion, Hook

@admin.register(Aplicacion)
class AplicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'app_id', 'link')
    readonly_fields = ('nombre', 'link')

@admin.register(Hook)
class HookAdmin(admin.ModelAdmin):
    list_display = ('path', 'application', 'trigger', 'module', 'uses')
    readonly_fields = ('hook_url', 'hook_id', 'uses')

# Register your models here.
