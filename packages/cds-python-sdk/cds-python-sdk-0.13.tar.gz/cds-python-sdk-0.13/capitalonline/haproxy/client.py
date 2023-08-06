# -*- coding: utf-8 -*-

from capitalonline.common.client import Client
from capitalonline.common.credential import Credential
from capitalonline.common.profile import http_profile, client_profile
from .models import DescribeZonesRequest, DescribeLoadBalancersSpecRequest, CreateLoadBalancerRequest, \
    DescribeLoadBalancersRequest, DescribeLoadBalancersModifySpecRequest, ModifyLoadBalancerInstanceSpecRequest, \
    DeleteLoadBalancerRequest, DescribeCACertificatesRequest, DescribeCACertificateRequest, DeleteCACertificateRequest, \
    UploadCACertificateRequest, DescribeLoadBalancerStrategysRequest, ModifyLoadBalancerStrategysRequest, \
    ModifyLoadBalancerNameRequest

ApiVersion = "2019-08-08"
SERVICE = 'lb'


def NewClient(secret_id, secret_key, region, timeout=60):
    """
    :param secret_id:
    :param secret_key:
    :param region:
    :param timeout:
    :return:
    """
    try:
        http_pf = http_profile.HttpProfile()
        http_pf.endpoint = 'cdsapi.capitalonline.net/lb/'
        http_pf.reqTimeout = timeout
        client_pf = client_profile.ClientProfile(httpProfile=http_pf)
        client_pf.signMethod = 'HMAC-SHA1'
        client = HaproxyClient(service=SERVICE, version=ApiVersion, credential=Credential(secret_id, secret_key),
                               region=region, profile=client_pf)

        return client, ''
    except Exception as e:
        return '', e


# 获取负载均衡Ha支持的区域
def NewDescribeZonesRequest():
    """
    :return:
    """
    request = DescribeZonesRequest(service=SERVICE, version=ApiVersion,
                                   action='DescribeZones')
    return request


# 获取某个站点支持的Haproxy产品类型以及规格
def NewDescribeLoadBalancersSpecRequest():
    """
    :return:
    """
    request = DescribeLoadBalancersSpecRequest(service=SERVICE, version=ApiVersion,
                                               action='DescribeLoadBalancersSpec')
    return request


# 创建Ha实例
def NewCreateLoadBalancerRequest():
    """
    :return:
    """
    request = CreateLoadBalancerRequest(service=SERVICE, version=ApiVersion,
                                        action='CreateLoadBalancer')
    return request


# 获取Ha实例列表
def NewDescribeLoadBalancersRequest():
    """
    :return:
    """
    request = DescribeLoadBalancersRequest(service=SERVICE, version=ApiVersion,
                                           action='DescribeLoadBalancers')
    return request


# 获取实例Ha的配置变更所支持的规格
def NewDescribeLoadBalancersModifySpecRequest():
    """
    :return:
    """
    request = DescribeLoadBalancersModifySpecRequest(service=SERVICE, version=ApiVersion,
                                                     action='DescribeLoadBalancersModifySpec')
    return request


# 修改实例规格
def NewModifyLoadBalancerInstanceSpecRequest():
    """
    :return:
    """
    request = ModifyLoadBalancerInstanceSpecRequest(service=SERVICE, version=ApiVersion,
                                                    action='ModifyLoadBalancerInstanceSpec')
    return request


# 删除Ha实例
def NewDeleteLoadBalancerRequest():
    """
    :return:
    """
    request = DeleteLoadBalancerRequest(service=SERVICE, version=ApiVersion,
                                        action='DeleteLoadBalancer')
    return request


# 获取用户的证书列表
def NewDescribeCACertificatesRequest():
    """
    :return:
    """
    request = DescribeCACertificatesRequest(service=SERVICE, version=ApiVersion,
                                            action='DescribeCACertificates')
    return request


# 获取用户的证书详
def NewDescribeCACertificateRequest():
    """
    :return:
    """
    request = DescribeCACertificateRequest(service=SERVICE, version=ApiVersion,
                                           action='DescribeCACertificate')
    return request


# 删除证书
def NewDeleteCACertificateRequest():
    """
    :return:
    """
    request = DeleteCACertificateRequest(service=SERVICE, version=ApiVersion,
                                         action='DeleteCACertificate')
    return request


# 添加证书
def NewUploadCACertificateRequest():
    """
    :return:
    """
    request = UploadCACertificateRequest(service=SERVICE, version=ApiVersion,
                                         action='UploadCACertificate')
    return request


# 获取Ha实例的当前监听的策略配置列表
def NewDescribeLoadBalancerStrategysRequest():
    """
    :return:
    """
    request = DescribeLoadBalancerStrategysRequest(service=SERVICE, version=ApiVersion,
                                                   action='DescribeLoadBalancerStrategys')
    return request


# 修改（删除、修改、添加）Ha实例的当前监听的策略配置列表
def NewModifyLoadBalancerStrategysRequest():
    """
    :return:
    """
    request = ModifyLoadBalancerStrategysRequest(service=SERVICE, version=ApiVersion,
                                                 action='ModifyLoadBalancerStrategys')
    return request


# 修改负载均衡名称
def NewModifyLoadBalancerNameRequest():
    """
    :return:
    """
    request = ModifyLoadBalancerNameRequest(service=SERVICE, version=ApiVersion,
                                            action='ModifyLoadBalancerName')
    return request


class HaproxyClient(Client):
    def __init__(self, service, version, credential, region, profile=None):
        super(HaproxyClient, self).__init__(service=service, version=version,
                                            credential=credential, region=region,
                                            profile=profile)
        # self.service = service
        # self.version = version
        # self.credential = credential
        # self.region = region
        # self.profile = profile

    def DescribeZones(self, request):
        """
        :param request: NewDescribeZonesRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeZonesRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(action=request.action, params=request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeLoadBalancersSpec(self, request):
        """
        :param request: NewDescribeLoadBalancersSpecRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeLoadBalancersSpecRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def CreateLoadBalancer(self, request):
        """
        :param request: NewCreateLoadBalancerRequest
        :return: response
        """
        try:
            if request is None:
                request = NewCreateLoadBalancerRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeLoadBalancers(self, request):
        """
        :param request: NewDescribeLoadBalancersRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeLoadBalancersRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeLoadBalancersModifySpec(self, request):
        """
        :param request: NewDescribeLoadBalancersModifySpecRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeLoadBalancersModifySpecRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def ModifyLoadBalancerInstanceSpec(self, request):
        """
        :param request: NewModifyLoadBalancerInstanceSpecRequest
        :return: response
        """
        try:
            if request is None:
                request = NewModifyLoadBalancerInstanceSpecRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DeleteLoadBalancer(self, request):
        """
        :param request: NewDeleteLoadBalancerRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDeleteLoadBalancerRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeCACertificates(self, request):
        """
        :param request: NewDescribeCACertificatesRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeCACertificatesRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeCACertificate(self, request):
        """
        :param request: NewDescribeCACertificateRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeCACertificateRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DeleteCACertificate(self, request):
        """
        :param request: NewDeleteCACertificateRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDeleteCACertificateRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def UploadCACertificate(self, request):
        """
        :param request: NewUploadCACertificateRequest
        :return: response
        """
        try:
            if request is None:
                request = NewUploadCACertificateRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def DescribeLoadBalancerStrategys(self, request):
        """
        :param request: NewDescribeLoadBalancerStrategysRequest
        :return: response
        """
        try:
            if request is None:
                request = NewDescribeLoadBalancerStrategysRequest()
            self.profile.httpProfile.reqMethod = 'GET'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def ModifyLoadBalancerStrategys(self, request):
        """
        :param request: NewModifyLoadBalancerStrategysRequest
        :return: response
        """
        try:
            if request is None:
                request = NewModifyLoadBalancerStrategysRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e

    def ModifyLoadBalancerName(self, request):
        """
        :param request: NewModifyLoadBalancerNameRequest
        :return: response
        """
        try:
            if request is None:
                request = NewModifyLoadBalancerNameRequest()
            self.profile.httpProfile.reqMethod = 'POST'
            response = self.call(request.action, request.to_params())
            return response, ''
        except Exception as e:
            return '', e
