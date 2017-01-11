#!/usr/bin/env python

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format
from solr_utils import exists_collection

import os


class ServiceCheck(Script):
    def service_check(self, env):
        pass

if __name__ == "__main__":
    ServiceCheck().execute()
