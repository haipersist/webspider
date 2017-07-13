#-*-coding:utf-8 -*-

import random
import requests
import json

def GetValidIP():
    try:
        r = requests.get('http://127.0.0.1:7000/?types=0&count=5&country=国内')
        addresses = json.loads(r.text)
        address = random.choice(addresses)
        ip,port = address[0],address[1]
        proxies={
            'http':'http://%s:%s'%(ip,port),
            'https':'http://%s:%s'%(ip,port)
        }
        return proxies
    except Exception,e:
        print str(e)
        return ()





