# !/usr/bin/python
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse


def sendReq():
    params = urllib.parse.urlencode({'echostr': 'word', 'signature': 'time',"timestamp":"2121","nonce":"1212"})
    url = 'http://127.0.0.1:5001/wechat?%s' % params
    with urllib.request.urlopen(url) as f:
        print(f.read().decode('utf-8'))


if __name__ == '__main__':
    sendReq()
