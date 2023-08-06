# -*- coding: utf-8 -*-
import os
import json

from capitalonline.common.abstract_client import AbstractClient
from capitalonline.common.exception.cds_sdk_exception import CdsSDKException


class Client(AbstractClient):

    def __init__(self, service, version, credential, region, profile=None):
        """
        :param credential: 接口调用凭证
        :type credential: capitalonline.common.credential.Credential
        :param region: 接口调用地域
        :type region: str
        :param version: 接口版本
        :type version: str
        :param service: 接口产品
        :type service: str
        :param profile: 请求网络信息
        :type profile: capitalonline.common.profile.client_profile.ClientProfile
        """
        if region is None or version is None or service is None:
            raise CdsSDKException("Client Parameter Error, "
                                  "credential region version service all required.")
        self._apiVersion = version
        self._service = service
        super(Client, self).__init__(credential, region, profile)