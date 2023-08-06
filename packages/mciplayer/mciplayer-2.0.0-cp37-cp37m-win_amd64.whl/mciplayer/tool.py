"""
Tool module for mciplayer
Do NOT import this module directly.
Instead, you should import the 'mciplayer' module.
"""
from ._mciwnd import *
from ._mciwnd_unicode import *
from functools import wraps
class MCIError(Exception):
    """
    Exception thrown when an internal MCI error occured.
    """
    pass
class SupportError(Exception):
    """
    Exception thrown when an operation in unsupported.
    """
    pass
def mciplayermethod(func):
    """
    A decorator for MCIPlayer methods.
    """
    @wraps(func)
    def dfunc(*args,**kwargs):
        val=func(*args,**kwargs)
        err=MCIWndGetError(args[0].wnd) if not args[0].use_utf8 else uMCIWndGetError(args[0].wnd)
        if err[0]:
            raise MCIError(err[1].decode('ansi' if not args[0].use_utf8 else 'utf-8'))
        return val
    return dfunc
