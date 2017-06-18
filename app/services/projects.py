#!/usr/local/env python
# -*- coding: utf-8 -*-

from .base import Base
from app.models import Project

class ProjectService(Base):
    __model__ = Project

    

projs = ProjectService()
# C:\Users\Public\Documents\Hyper-V\Virtual Hard Disks\MobyLinuxVM.vhdx