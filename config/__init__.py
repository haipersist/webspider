#!/usr/bin/env python
#-coding:utf-8 -*-



import os
import sys
from .dbsetting import DATABASES
from .envvar import SPIDERPATH,EMAIL,EMAIL_VAR
from .websetting import AUTH








def init_env():
    """
    the function is used to set project environment variables and
    python search path
    :return:
    """
    os.environ.setdefault('SPIDERPATH',SPIDERPATH)
    sys.path.append(SPIDERPATH)
    print os.environ.get("SPIDERPATH")
    os.environ.setdefault('EMAIL',EMAIL_VAR)
    #print os.environ.get("EMAIL")
