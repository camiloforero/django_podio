# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    #url(r'^personas/(?P<pk>\d+)/registrar$', views.registrar, name='registrar'),
    #url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^app/(?P<appID>\d+)/$', views.ver_aplicacion, name='ver_aplicacion'),
    url(r'^app/(?P<appID>\d+)/items/$', views.ver_items, name='ver_items'),
    url(r'^app/(?P<appID>\d+)/items/(?P<itemID>\d+)/$', views.ver_item, name='ver_item'),
    url(r'^hooks/(?P<hookName>\w+)/$', csrf_exempt( views.HookView.as_view() ), name='hooks'),
]

