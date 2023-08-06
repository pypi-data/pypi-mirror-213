from __future__ import annotations

from time import time, sleep
from datetime import datetime, timezone, timedelta
from email import utils

from . import request, const

def getwebtime(timeout=0.0, UTCdiff: int=None) -> datetime | None:
    if UTCdiff is not None:
        UTCdiff = timezone(timedelta(hours=UTCdiff))
    tstart = time()
    while True:
        reply = request.get(
            'http://www.baidu.com', timeout=1,
            proxies=dict(http=None, https=None),
            headers={'User-Agent': const.ARG_DEFAULT_AGENT})
        if reply.status_code == 200:
            return utils.parsedate_to_datetime(reply.headers.get('date')).astimezone(UTCdiff)
        if timeout and time() - tstart > timeout:
            break
        sleep(1)
