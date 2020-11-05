# !/usr/bin/python
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse


def sendReq():
    params = urllib.parse.urlencode(
        {'echostr': 'word', 'test': True, 'signature': 'time', "timestamp": "2121", "nonce": "1212"})
    url = 'http://115.159.197.227:80/?%s' % params
    # url = 'http://localhost:80/?%s' % params
    with urllib.request.urlopen(url) as f:
        print(f.read().decode('utf-8'))


if __name__ == '__main__':
    sendReq()
