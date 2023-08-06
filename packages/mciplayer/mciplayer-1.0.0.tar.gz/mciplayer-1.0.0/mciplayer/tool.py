"""
Tool module for mciplayer
"""
from ._mciwnd import *
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
        err=MCIWndGetError(args[0].wnd)
        if err[0]:
            raise MCIError(err[1].decode('ansi'))
        return val
    return dfunc