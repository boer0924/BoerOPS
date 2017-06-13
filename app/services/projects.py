#!/usr/local/env python
# -*- coding: utf-8 -*-

from app.models import Projects

class ProjectsService(Base):
    __model__ = Projects

    

projects = ProjectsService()