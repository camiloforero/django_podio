# -*- coding: utf-8 -*-
"""
Module containing the HookDispatcher class and its custom exception
"""
import importlib

class HookException(Exception):
    """
    Simple exception specialized for hook errors
    """
    pass

class HookDispatcher(object):
    """
        This class is in charge of loading the right module that should handle a PODIO hook and returning it to the view so it can use it further.
    """

    PAIRINGS = {'14549345': 'mailEntrevista'} #This will eventually be replaced by something else that can be modified without directly changing the code

    def __init__(self, hookName, module):
        self.hookName = hookName
        self.module = importlib.import_module('.%s' % module, 'podioHooks')

    def test(self):
        """
        Prints instance variables to see it is working correctly
        """
        print self.hookName
        print self.module
