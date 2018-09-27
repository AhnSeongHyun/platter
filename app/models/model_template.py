# -*- coding:utf-8 -*-
from enum import Enum
from sqlalchemy import Column, Integer, Text, String, Boolean

from {{app}}.models.base import MixinBase
from {{app}}.extensions import db


class {{resource}}(db.Model, MixinBase):
    __tablename__ = 'tb_{{resource}}'
    __table_args__ = {'extend_existing': True, "mysql_engine": "InnoDB"}

    def __repr__(self):
        return str(vars(self))