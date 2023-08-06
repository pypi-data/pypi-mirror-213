
ARG_DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
MSG_FAIL = 'fail'
MSG_SUCCESS = 'success'
MSG_FREQUENT = 'frequent'
MSG_FORBIDDEN = 'forbidden'
MSG_NOT_FOUND = 'not found'
ERR_TIMEOUT = 'timeout'
ERR_BAD_NETWORK = 'bad network'
ERR_CERTIFICATE_EXPIRED = 'certificate expired'

MAKEARG_NOPROXY = lambda: dict(http=None, https=None)
