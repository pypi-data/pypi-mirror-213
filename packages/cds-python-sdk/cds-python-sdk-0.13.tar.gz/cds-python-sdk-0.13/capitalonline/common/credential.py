# -*- coding: utf-8 -*-

import json
import os
import time
try:
    # py3
    import configparser
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    # py2
    import ConfigParser as configparser
    from urllib import urlencode
    from urllib import urlopen

from capitalonline.common.exception.cds_sdk_exception import CdsSDKException


class Credential(object):
    def __init__(self, secret_id, secret_key, token=None):
        """CDS Credentials.

        :param secret_id: The secret id of your credential.
        :type secret_id: str
        :param secret_key: The secret key of your credential.
        :type secret_key: str
        :param token: The federation token of your credential, if this field
                      is specified, secret_id and secret_key should be set
                      accordingly.
        """
        if secret_id is None or secret_id.strip() == "":
            raise CdsSDKException("InvalidCredential", "secret id should not be none or empty")
        if secret_id.strip() != secret_id:
            raise CdsSDKException("InvalidCredential", "secret id should not contain spaces")
        self.secret_id = secret_id

        if secret_key is None or secret_key.strip() == "":
            raise CdsSDKException("InvalidCredential", "secret key should not be none or empty")
        if secret_key.strip() != secret_key:
            raise CdsSDKException("InvalidCredential", "secret key should not contain spaces")
        self.secret_key = secret_key

        self.token = token

    @property
    def secretId(self):
        return self.secret_id

    @property
    def secretKey(self):
        return self.secret_key