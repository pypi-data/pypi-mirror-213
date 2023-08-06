from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from requests import Response

from . import request
from .const import *

import os, time

class GiteePages(object):
    def __init__(self, repourl: str, dstbranch: str, dstdir: str, cookie: str, token: str, logfile='updatetime'):
        self.__url = f'{repourl}/pages/rebuild'
        self.__data = dict(branch=str(dstbranch), build_directory=str(dstdir), auto_update='false')
        self.__headers = {'Cookie': cookie, 'X-Csrf-Token': token, 'User-Agent': ARG_DEFAULT_AGENT}
        self.__logfile = logfile

    @classmethod
    def fromuser(cls, usrname: str, repo: str, dstbranch: str, dstdir: str, cookie: str, token: str, logfile='updatetime'):
        return cls(f'https://gitee.com/{usrname}/{repo}', dstbranch, dstdir, cookie, token, logfile)

    @property
    def updatetime(self) -> float:
        if not os.path.isfile(self.__logfile):
            return 0.0
        with open(self.__logfile, 'r') as log:
            return float(log.read())

    @property
    def updatecd(self) -> float:
        return max(0.0, 62 - (time.time() - self.updatetime))

    def update(self, https=True, waitcd=True) -> Literal['success', 'frequent'] | request.Error | Response:
        updatecd = waitcd and self.updatecd
        if updatecd:
            print(f'一分钟内有更新操作，下次更新时间为{updatecd}s后，等待中...')
            time.sleep(updatecd)
            print('正在更新......')
        data = {'force_https': str(https).lower(), **self.__data}
        reply = request.post(self.__url, data, headers=self.__headers, timeout=2, proxies=MAKEARG_NOPROXY())
        if reply.status_code == 200 and reply.text.find('正在') > -1:
            os.makedirs(os.path.dirname(self.__logfile), exist_ok=True)
            with open(self.__logfile, 'w') as log:
                log.write(str(time.time()))
            return MSG_SUCCESS
        if reply.status_code == 200 and reply.text.find('频繁') > -1:
            return MSG_FREQUENT
        return reply
