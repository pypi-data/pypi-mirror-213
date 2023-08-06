# -*- coding: utf-8 -*-

import binascii
import hashlib
import hmac
import sys
import time
import uuid
#import urllib
import base64
from hashlib import sha1
try:
    import urllib.parse as urlparse
except ImportError:
    import urllib as urlparse

from capitalonline.common.exception.cds_sdk_exception import CdsSDKException


class Sign(object):

    @staticmethod
    def sign(secret_key, sign_str, sign_method):
        if sys.version_info[0] > 2:
            sign_str = bytes(sign_str, 'utf-8')
            secret_key = bytes(secret_key, 'utf-8')

        digestmod = None
        if sign_method == 'HmacSHA256':
            digestmod = hashlib.sha256
        elif sign_method == 'HMAC-SHA1':
            digestmod = hashlib.sha1
        else:
            raise CdsSDKException("signMethod invalid", "signMethod only support (HmacSHA1, HmacSHA256)")

        hashed = hmac.new(secret_key, sign_str, digestmod)
        base64 = binascii.b2a_base64(hashed.digest())[:-1]

        if sys.version_info[0] > 2:
            base64 = base64.decode()
        return base64

    @staticmethod
    def get_signature(action, ak, access_key_secret, method, url, param={}):
        """
        @params: action: 接口动作
        @params: ak: ak值
        @params: access_key_secret: ak秘钥
        @params: method: 接口调用方法(POST/GET)
        @params: param: 接口调用Query中参数(非POST方法Body中参数)
        @params: url: 接口调用路径
        """
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        D = {
            'Action': action,
            'AccessKeyId': ak,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'SignatureVersion': "1.0",
            "Timestamp": timestamp,
            'Version': '2019-08-08',
        }

        if param:
            D.update(param)

        sortedD = sorted(D.items(), key=lambda x: x[0])
        canstring = ''
        for k, v in sortedD:
            canstring += '&' + percentEncode(k) + '=' + percentEncode(v)
        stringToSign = method + '&%2F&' + percentEncode(canstring[1:])
        h = hmac.new(access_key_secret.encode('utf-8'), stringToSign.encode('utf-8'), sha1)
        signature = base64.encodestring(h.digest()).strip()
        D['Signature'] = signature
        url = url + '/?' + urlparse.urlencode(D)
        return url


def percentEncode(s):
    if type(s) != str:
        res = urlparse.quote(s.decode(sys.stdin.encoding).encode('utf-8'), '')
    else:
        res = urlparse.quote(s.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res
