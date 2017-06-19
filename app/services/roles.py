#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import Base
from app.models import Role

class RoleService(Base):
    __model__ = Role

roles = RoleService()