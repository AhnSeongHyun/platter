# -*- coding:utf-8 -*-

from flask import jsonify

from basetype import EnumMeta
from beat_api.resources.app_message import app_message_db_manager
from beat_lang_code import BeatLangCode


class HttpStatusCode(object):
    __metaclass__ = EnumMeta

    SUCCESS = 20000
    INVALID_PARAMETER = 40000
    INVALID_HEADER = 40001
    INVALID_AUTHORIZATION = 40100
    EXPIRED_TOKEN = 40101
    INVALID_TOKEN = 40102
    MISSING_HEADER = 40103
    PERMISSION_DENIED = 40104

    NOT_FOUND = 40400
    INTERNAL_SERVER_ERROR = 50000


class ResponseBase(object):
    def to_dict(self):
        raise NotImplementedError("Need Implementation")


class ResponseData(ResponseBase):
    meta = None
    data = None

    def __init__(self, code=HttpStatusCode.SUCCESS, success_msg_code=HttpStatusCode.SUCCESS, lang=BeatLangCode.KO, data=None):
        self.meta = Meta(code=code, success_msg_code=success_msg_code, lang=lang)
        self.data = data

    def to_dict(self):
        result = dict()
        result["meta"] = self.meta.__dict__
        if self.data is not None:
            result["data"] = self.data
        return result

    @property
    def json(self):
        http_status_code = int(str(self.meta.code)[:3])
        return jsonify(self.to_dict()), http_status_code


class Meta(object):
    code = None
    message = None
    msg = None

    def __init__(self, code=HttpStatusCode.SUCCESS, success_msg_code=None, lang=BeatLangCode.KO):
        self.code = code
        self.message = HttpStatusCode[self.code]
        self.msg = ''
        app_msg = None
        if self.code == HttpStatusCode.SUCCESS:
            if success_msg_code:  # 성공 메시지 코드가 있으면 가져온다.
                app_msg = app_message_db_manager.select_app_message(status_code=HttpStatusCode[success_msg_code],
                                                                    lang=lang)
        else:
            app_msg = app_message_db_manager.select_app_message(status_code=HttpStatusCode[self.code],
                                                                lang=lang)

        if app_msg:
            self.msg = app_msg.msg
