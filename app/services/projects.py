#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import Base
from app.models import Project
from .hosts import hosts

class ProjectService(Base):
    __model__ = Project

    

projs = ProjectService()
# C:\Users\Public\Documents\Hyper-V\Virtual Hard Disks\MobyLinuxVM.vhdx   