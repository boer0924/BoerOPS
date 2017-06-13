#!/usr/local/env python
# -*- coding: utf-8 -*-

from app.models import Hosts

class HostsService(Base):
    __model__ = Hosts

hosts = HostsService()