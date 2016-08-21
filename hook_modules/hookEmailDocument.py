# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.template import Template, Context
from django_podio import api, tools
from django_documents import documentsApi
from django_mailTemplates import mailApi
from complex_hooks.scripts import email_document
import pdb

def run(appID, params, hook=None):
    ans = ""
    hook = hook.email_document_hook
    podioApi = api.PodioApi(appID, client=hook.podio_user_client)
    item = podioApi.get_item(params['item_id'], external_id=False, no_html=True, depth=2)
    email_document(item, hook)
        
