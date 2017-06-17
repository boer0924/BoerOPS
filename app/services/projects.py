#!/usr/local/env python
# -*- coding: utf-8 -*-

from app.models import Project

class ProjectService(Base):
    __model__ = Project

    

projects = ProjectService()
# C:\Users\Public\Documents\Hyper-V\Virtual Hard Disks\MobyLinuxVM.vhdx