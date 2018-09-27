# -*- coding:utf-8 -*-
from attrdict import AttrDict
from flask import render_template
from flask import Blueprint, g, request, current_app
from datetime import timedelta, datetime
from {{app}}.commons.logger import logger
from {{app}}.resources.response_data import ResponseData, HttpStatusCode

{{resource}}_view = Blueprint('{{resource}}_view', __name__, url_prefix='/view/{{resource}}')


@{{resource}}_view.route('/test', methods=['GET'])
def {{resource}}_view_test():
    return "TEST"


@{{resource}}_view.route('/', methods=['GET'])
def {{resource}}_view():
    return render_template("{{resource}}/index.html")