# -*- coding: utf-8 -*-
import importlib
from podioHooks import mailEntrevista

class HookException(Exception):
    pass

class HookDispatcher:
    """
        This class is in charge of loading the right module that should handle a PODIO hook and returning it to the view so it can use it further.
    """

    PAIRINGS = {'14549345': 'mailEntrevista'} #This will eventually be replaced by something else that can be modified without directly changing the code

    def __init__(self, hookName, module):
        self.hookName = hookName
        self.module = importlib.import_module('.%s' % module, 'podioHooks')

    def test(self):
        
        print self.hookName
        print self.module




