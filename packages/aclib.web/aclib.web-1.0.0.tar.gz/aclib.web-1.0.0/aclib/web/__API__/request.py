from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, TypeVar, ParamSpec
    T = TypeVar('T')
    P = ParamSpec('P')

from .const import *

from functools import wraps

import sys, requests


class Error(object):

    def __init__(self):
        exctype, excobject, traceback = sys.exc_info()
        self.status_code = 0
        self.error = excobject
        self.traceback = traceback
        self.text = f'{str(exctype)[8:-2]}: {excobject}'
        self.content = self.text.encode()
        self.message = self.text
        if self.text.find('certificate has expired') > -1:
            self.message = ERR_CERTIFICATE_EXPIRED
        if isinstance(self.error, requests.exceptions.ConnectionError):
            self.message = ERR_BAD_NETWORK
        if isinstance(self.error, requests.exceptions.Timeout):
            self.message = ERR_TIMEOUT

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}-{self.status_code} {self.message}>'


def new_request(func: Callable[P, T]) -> Callable[P, T | Error]:
    @wraps(func)
    def wrapped_request(*args: P.args, **kwargs: P.kwargs) -> T | Error:
        try: return func(*args, **kwargs)
        except: return Error()
    return wrapped_request


get      = new_request(requests.get)
post     = new_request(requests.post)
head     = new_request(requests.head)
delete   = new_request(requests.delete)
put      = new_request(requests.put)
patch    = new_request(requests.patch)
options  = new_request(requests.options)
