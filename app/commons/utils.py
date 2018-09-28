# -*- coding:utf-8 -*-

from datetime import datetime, timedelta

import arrow
from validate_email import validate_email as validate_user_email


def today_st_ed():
    """
    현재시점 오늘하루시간
    2016/11/23 19:00:00 => st = 2016/11/23 00:00:00, ed = 2016/11/24 00:00:00
    :return:
    """
    today = datetime.today()
    today_yyyymmdd = today.strftime("%Y%m%d")
    tomorrow_yyyymmdd = (today + timedelta(days=1)).strftime("%Y%m%d")

    st = today_yyyymmdd + " 00:00:00"
    ed = tomorrow_yyyymmdd + " 00:00:00"

    return datetime.strptime(st, "%Y%m%d %H:%M:%S"), datetime.strptime(ed, "%Y%m%d %H:%M:%S")


def today_duration():
    now = datetime.now()
    st = datetime.strptime(now.strftime('%Y%m%d 00:00:00'), '%Y%m%d %H:%M:%S')
    ed = datetime.strptime((now + timedelta(days=1)).strftime('%Y%m%d 00:00:00'), '%Y%m%d %H:%M:%S')
    return st, ed


def day_ago_duration(d):
    ed = datetime.now()
    return arrow.get(ed).replace(days=-1 * d).datetime, ed


def month_ago_duration(m):
    ed = datetime.now()
    return arrow.get(ed).replace(months=-1 * m).datetime, ed


def week_ago_duration(w):
    ed = datetime.now()
    return arrow.get(ed).replace(weeks=-1 * w).datetime, ed


def year_ago_duration(y):
    ed = datetime.now()
    return arrow.get(ed).replace(years=-1 * y).datetime, ed


def check_required(required, inspected_dict):
    """
    :param required: 필수 요소 list
    :param inspected_dict: 검사 대상 dict
    :return: 필수요소 여부
    """
    if isinstance(required, list) and isinstance(inspected_dict, dict):
        intersected = set(required).intersection(set(inspected_dict.keys()))
        if len(intersected) == len(required):
            return True
        else:
            return False
    else:
        raise TypeError("required : %s, inspected_dict : %s  ", str(type(required)), str(type(inspected_dict)))


def validate_email(email):
    """
    :param email: 검사대상 email
    :return: True or False
    """
    return validate_user_email(email)


def myself():
    import inspect
    try:
        me = inspect.stack()[1][3]
        return me
    except BaseException:
        return None
