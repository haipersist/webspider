#-*-coding:utf-8 -*-

import os
from fabric.api import local,lcd




def pushcode(msg):
    with lcd(os.path.join(os.path.abspath('.'))):
        local("git commit -m %s"% msg)
        local(("git push origin master"))



