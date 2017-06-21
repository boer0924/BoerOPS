#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import Base
from app.models import Deploy

class DeployService(Base):
    __model__ = Deploy

    ENV = {
        'test30': 0,
        'test31': 1,
        'prod': 2
    }

    def _deploy_task(self, project_id):
        pass

    def deploy_test(self, deploy):
        pass

    def deploy_prod(self, deploy):
        pass
    
    def rollback(self, deploy):
        pass

deploys = DeployService()