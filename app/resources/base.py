# -*- coding:utf-8 -*-
import traceback
from functools import wraps

from flask import g
from flask import request

from {{app}}.commons.logger import logger
from {{app}}.{{resource}}.response_data import ResponseData, HttpStatusCode
from {{app}}.commons.sentry import client


def exception_handler(func):
    """
    :param func: VIEW/API
    :return: HTTP RESPONSE
    """
    @wraps(func)
    def new_func(*args, **kwargs):

        logger.debug('[{}]{} HEADER:{}'.format(request.method, request.url, request.headers))

        lang = 'ko'
        if hasattr(g, 'lang'):
            lang = g.lang
        try:
            result = func(*args, **kwargs)
        except BaseException:
            logger.exception(traceback.format_exc())
            client.captureException()
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR, lang=lang).json
        return result
    return new_func
