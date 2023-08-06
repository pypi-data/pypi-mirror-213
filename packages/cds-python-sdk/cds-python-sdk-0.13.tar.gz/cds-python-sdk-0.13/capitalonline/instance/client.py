# -*- coding: utf-8 -*-

from capitalonline.common.client import Client
from .models import AddInstanceRequest, DescribeInstanceRequest, DeleteInstanceRequest, ModifyInstanceNameRequest, \
    ModifyInstanceSpecRequest, CreateDiskRequest, ResizeDiskRequest, DeleteDiskRequest, ModifyIpRequest, \
    ExtendSystemDiskRequest, ResetInstancesPasswordRequest, ResetImageRequest, ModifyInstanceChargeTypeRequest, \
    StopInstanceRequest, RebootInstanceRequest, StartInstanceRequest, StartInstancesRequest, StopInstancesRequest, \
    RebootInstancesRequest
import json
from capitalonline.common.profile import http_profile, client_profile
from capitalonline.common.credential import Credential

ApiVersion = "2019-08-08"
SERVICE = 'ccs'


def NewClient(secret_id, secret_key, region, timeout=60):
    """
    :param secret_key:
    :param secret_id:
    :param region:
    :param timeout:
    :return:
    """
    credential = Credential(secret_id, secret_key)
    http_pf = http_profile.HttpProfile()
    http_pf.endpoint = 'cdsapi.capitalonline.net/ccs/'
    http_pf.reqMethod = 'POST'
    http_pf.reqTimeout = timeout
    client_pf = client_profile.ClientProfile(httpProfile=http_pf)
    client_pf.signMethod = 'HMAC-SHA1'
    try:
        client = InstanceClient(service=SERVICE, version=ApiVersion, credential=credential,
                                region=region, profile=client_pf)
        return client, ''
    except Exception as e:
        return '', e


def NewAddInstanceRequest():
    """
    :return:
    """
    request = AddInstanceRequest(service=SERVICE, version=ApiVersion,
                                 action='CreateInstance')
    return request


def NewDescribeInstanceRequest():
    """
    :return:
    """
    request = DescribeInstanceRequest(service=SERVICE, version=ApiVersion,
                                      action='DescribeInstances')
    return request


def NewDeleteInstanceRequest():
    """
    :return:
    """
    request = DeleteInstanceRequest(service=SERVICE, version=ApiVersion,
                                    action='DeleteInstance')
    return request


def NewModifyInstanceNameRequest():
    request = ModifyInstanceNameRequest(service=SERVICE, version=ApiVersion,
                                        action='ModifyInstanceName')
    return request


def NewModifyInstanceSpecRequest():
    request = ModifyInstanceSpecRequest(service=SERVICE, version=ApiVersion,
                                        action='ModifyInstanceSpec')
    return request


def NewCreateDiskRequest():
    request = CreateDiskRequest(service=SERVICE, version=ApiVersion,
                                action='CreateDisk')
    return request


def NewResizeDiskRequest():
    request = ResizeDiskRequest(service=SERVICE, version=ApiVersion,
                                action='ResizeDisk')
    return request


def NewDeleteDiskRequest():
    request = DeleteDiskRequest(service=SERVICE, version=ApiVersion,
                                action='DeleteDisk')
    return request


def NewModifyIpRequest():
    request = ModifyIpRequest(service=SERVICE, version=ApiVersion,
                              action='ModifyIpAddress')
    return request


def NewExtendSystemDiskRequest():
    request = ExtendSystemDiskRequest(service=SERVICE, version=ApiVersion,
                                      action='ExtendSystemDisk')
    return request


def NewResetInstancesPasswordRequest():
    request = ResetInstancesPasswordRequest(service=SERVICE, version=ApiVersion,
                                            action='ResetInstancesPassword')
    return request


def NewResetImageRequest():
    request = ResetImageRequest(service=SERVICE, version=ApiVersion,
                                action='ResetImage')
    return request


def NewModifyInstanceChargeTypeRequest():
    request = ModifyInstanceChargeTypeRequest(service=SERVICE, version=ApiVersion,
                                              action='ModifyInstanceChargeType')
    return request


def NewStopInstanceRequest():
    request = StopInstanceRequest(service=SERVICE, version=ApiVersion,
                                  action='StopInstance')
    return request


def NewRebootInstanceRequest():
    request = RebootInstanceRequest(service=SERVICE, version=ApiVersion,
                                    action='RebootInstance')
    return request


def NewStartInstanceRequest():
    request = StartInstanceRequest(service=SERVICE, version=ApiVersion,
                                   action='StartInstance')
    return request


def NewStartInstancesRequest():
    request = StartInstancesRequest(service=SERVICE, version=ApiVersion,
                                    action='StartInstances')
    return request


def NewStopInstancesRequest():
    request = StopInstancesRequest(service=SERVICE, version=ApiVersion,
                                   action='StopInstances')
    return request


def NewRebootInstancesRequest():
    request = RebootInstancesRequest(service=SERVICE, version=ApiVersion,
                                     action='RebootInstances')
    return request


class InstanceClient(Client):
    def __init__(self, service, version, credential, region, profile=None):
        super().__init__(service=service, version=version, credential=credential,
                         region=region, profile=profile)

    def CreateInstance(self, request):
        """
        :param request: NewAddInstanceRequest
        :return: response
        """
        try:
            if request is None:
                request = NewAddInstanceRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DescribeInstance(self, request):
        """
        :param request:
        :return:
        """
        try:
            if request is None:
                request = NewDescribeInstanceRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeleteInstance(self, request):
        try:
            if request is None:
                request = NewDeleteInstanceRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyInstanceName(self, request):
        try:
            if request is None:
                request = NewModifyInstanceNameRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyInstanceSpec(self, request):
        try:
            if request is None:
                request = NewModifyInstanceSpecRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def CreateDisk(self, request):
        try:
            if request is None:
                request = NewCreateDiskRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ResizeDisk(self, request):
        try:
            if request is None:
                request = NewResizeDiskRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def DeleteDisk(self, request):
        try:
            if request is None:
                request = NewDeleteDiskRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyIpAddress(self, request):
        try:
            if request is None:
                request = NewModifyIpRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ExtendSystemDisk(self, request):
        try:
            if request is None:
                request = NewExtendSystemDiskRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ResetInstancesPassword(self, request):
        try:
            if request is None:
                request = NewResetInstancesPasswordRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ResetImage(self, request):
        try:
            if request is None:
                request = NewResetImageRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def ModifyInstanceChargeType(self, request):
        try:
            if request is None:
                request = NewModifyInstanceChargeTypeRequest()
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def StopInstance(self, request):
        try:
            if request is None:
                request = NewStopInstanceRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def RebootInstance(self, request):
        try:
            if request is None:
                request = NewRebootInstanceRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def StartInstance(self, request):
        try:
            if request is None:
                request = NewStartInstanceRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def StartInstances(self, request):
        try:
            if request is None:
                request = NewStartInstancesRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def StopInstances(self, request):
        try:
            if request is None:
                request = NewStopInstancesRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e

    def RebootInstances(self, request):
        try:
            if request is None:
                request = NewRebootInstancesRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return json.loads(response), ''
        except Exception as e:
            return '', e
