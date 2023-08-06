# -*- coding: utf-8 -*-

import json

from capitalonline.common import credential
from capitalonline.common.client import Client
from capitalonline.common.profile import http_profile, client_profile
from capitalonline.vdc.model import DescVdcRequest, CreateVdcRequest, DeleteVdcRequest, \
    CreatePublicNetworkRequest, CreatePrivateNetworkRequest, ModifyPublicNetworkRequest, \
    DeletePublicIpRequest, DeletePublicNetworkRequest, \
    DeletePrivateNetworkRequest, RenewPublicNetworkRequest, ModifyVdcNameRequest, AddPublicIpRequest


def NewClient(secret_id, secret_key, region, timeout=60):
    """
    :param secret_id:  secret id
    :type secret_id: str
    :param secret_key: secret key
    :type secret_key: str
    :param region: region info
    :type region: str
    :param timeout: request timeout, default 60
    :type timeout: int

    """
    http_pf = http_profile.HttpProfile()
    http_pf.endpoint = 'cdsapi.capitalonline.net/network/'
    http_pf.reqTimeout = timeout
    http_pf.reqMethod = 'GET'
    client_pf = client_profile.ClientProfile(httpProfile=http_pf)
    client_pf.signMethod = 'HMAC-SHA1'
    cre = credential.Credential(secret_id=secret_id,
                                secret_key=secret_key)

    return VdcClient(cre, region, client_pf)


class VdcClient:
    SERVICE = 'network'
    ApiVersion = "2019-08-08"

    def __init__(self, credential, region, profile):
        """
        :param credential: api call certificate
        :type credential: capitalonline.common.credential.Credential
        :param region: api call region
        :type region: str
        :param profile: request info
        :type profile: capitalonline.common.profile.client_profile.ClientProfile
        """
        client = Client(service=self.SERVICE, version=self.ApiVersion,
                        credential=credential, region=region, profile=profile)
        self.client = client

    def DescribeVdc(self, request: DescVdcRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def CreateVdc(self, request: CreateVdcRequest):
        try:
            self.client.profile.httpProfile.reqMethod = "POST"
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeleteVdc(self, request: DeleteVdcRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def CreatePublicNetwork(self, request: CreatePublicNetworkRequest):
        try:
            self.client.profile.httpProfile.reqMethod = "POST"
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def CreatePrivateNetwork(self, request: CreatePrivateNetworkRequest):
        try:
            self.client.profile.httpProfile.reqMethod = "POST"
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyPublicNetwork(self, request: ModifyPublicNetworkRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def AddPublicIp(self, request: AddPublicIpRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeletePublicIp(self, request: DeletePublicIpRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeletePublicNetwork(self, request: DeletePublicNetworkRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeletePrivateNetwork(self, request: DeletePrivateNetworkRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def RenewPublicNetwork(self, request: RenewPublicNetworkRequest):
        try:
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyVdcName(self, request: ModifyVdcNameRequest):
        try:
            self.client.profile.httpProfile.reqMethod = "POST"
            response = self.client.call(action=request.ACTION, params=request.to_param())
            return json.loads(response), ''
        except Exception as e:
            return '', e
