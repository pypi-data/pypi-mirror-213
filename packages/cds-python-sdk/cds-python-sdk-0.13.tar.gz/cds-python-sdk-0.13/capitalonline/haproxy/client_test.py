# -*- coding: utf-8 -*-

import json

from capitalonline.haproxy.client import NewClient, NewDescribeZonesRequest, NewDescribeLoadBalancersSpecRequest, \
    NewCreateLoadBalancerRequest, NewDescribeLoadBalancersRequest, NewDescribeLoadBalancersModifySpecRequest, \
    NewModifyLoadBalancerInstanceSpecRequest, NewDeleteLoadBalancerRequest, NewDescribeCACertificatesRequest, \
    NewDescribeCACertificateRequest, NewDeleteCACertificateRequest, NewUploadCACertificateRequest, \
    NewDescribeLoadBalancerStrategysRequest, NewModifyLoadBalancerStrategysRequest, NewModifyLoadBalancerNameRequest

ak = ""
sk = ""
Beijing_region = ''
reqTimeout = 60


def TestClient_DescribeZones():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeZonesRequest()
    response, err = client.DescribeZones(request)
    print(f"DescribeZones response {response}, err: {err}")


def TestClient_DescribeLoadBalancersSpec():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeLoadBalancersSpecRequest()
    request.RegionId = ""
    response, err = client.DescribeLoadBalancersSpec(request)
    print(f"DescribeLoadBalancersSpec response {response}, err: {err}")


def TestClient_CreateLoadBalancer():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewCreateLoadBalancerRequest()
    request.RegionId = ""
    request.VdcId = ''
    request.BasePipeId = ''
    request.InstanceName = 'test-sdk-haproxy'
    request.PaasGoodsId = 1
    request.Ips = [
        {
            "PipeType": "private",
            "PipeId": "",
            "IsVip": 1
        }
    ]
    request.Amount = 3
    response, err = client.CreateLoadBalancer(request)
    print(f"CreateLoadBalancer response {response}, err: {err}")


def TestClient_DescribeLoadBalancers():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeLoadBalancersRequest()
    # request.InstanceName = "test"

    response, err = client.DescribeLoadBalancers(request)
    print(f"DescribeLoadBalancersSpec response {response}, err: {err}")


def TestClient_DescribeLoadBalancersModifySpec():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeLoadBalancersModifySpecRequest()
    request.InstanceUuid = ""
    response, err = client.DescribeLoadBalancersModifySpec(request)
    print(f"DescribeLoadBalancersModifySpec response {response}, err: {err}")


def TestClient_ModifyLoadBalancerInstanceSpec():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyLoadBalancerInstanceSpecRequest()
    request.InstanceUuid = ""
    request.PaasGoodsId = 1
    response, err = client.ModifyLoadBalancerInstanceSpec(request)
    print(f"ModifyLoadBalancerInstanceSpec response {response}, err: {err}")


def TestClient_DeleteLoadBalancer():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDeleteLoadBalancerRequest()
    request.InstanceUuid = ""
    response, err = client.DeleteLoadBalancer(request)
    print(f"DeleteLoadBalancer response {response}, err: {err}")


def TestClient_DescribeCACertificates():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeCACertificatesRequest()
    response, err = client.DescribeCACertificates(request)
    print(f"DescribeCACertificates response {response}, err: {err}")


def TestClient_DescribeCACertificate():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeCACertificateRequest()
    request.CertificateId = ""
    response, err = client.DescribeCACertificate(request)
    print(f"DescribeCACertificate response {response}, err: {err}")


def TestClient_DeleteCACertificate():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDeleteCACertificateRequest()
    request.CertificateId = ""
    response, err = client.DeleteCACertificate(request)
    print(f"DeleteCACertificate response {response}, err: {err}")


def TestClient_UploadCACertificate():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewUploadCACertificateRequest()
    request.Certificate = ""
    request.PrivateKey = ""
    request.CertificateName = 'test_sdk_23_05_22'
    response, err = client.UploadCACertificate(request)
    print(f"UploadCACertificate response {response}, err: {err}")


def TestClient_DescribeLoadBalancerStrategys():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeLoadBalancerStrategysRequest()
    request.InstanceUuid = ""
    response, err = client.DescribeLoadBalancerStrategys(request)
    print(f"DescribeLoadBalancerStrategys response {response}, err: {err}")


def TestClient_ModifyLoadBalancerStrategys():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyLoadBalancerStrategysRequest()
    request.InstanceUuid = ""
    request.HttpListeners = [
        {
            "ServerTimeoutUnit": "",
            "ServerTimeout": "",
            "StickySession": "",
            "AclWhiteList": [
                ""
            ],
            "Option": {
                "Httpchk": {
                    'Method': "GET",
                    "Uri": ''
                }
            },
            "SessionPersistence": {
                "Key": "test123",
                "Mode": 2,
                "Timer": {
                    "MaxIdle": 3,
                    "MaxLife": 3
                }
            },
            "CertificateIds": [
                {
                    "CertificateId": "",
                    "CertificateName": "test"
                }
            ],
            "ListenerMode": "http",
            "MaxConn": 1,
            "ConnectTimeoutUnit": "ms",
            "Scheduler": "",
            "BackendServer": [
                {
                    "IP": "",
                    "Port": 1,
                    "Weight": "",
                    "MaxConn": 1
                }
            ],
            "ConnectTimeout": "1000",
            "ClientTimeout": "1000",
            "ListenerName": "",
            "ClientTimeoutUnit": "ms",
            "ListenerPort": 1
        }
    ]
    request.TcpListeners = [
        {
            "ServerTimeoutUnit": "ms",
            "AclWhiteList": [],
            "ListenerMode": "tcp",
            "ListenerName": "",
            "Scheduler": "",
            "MaxConn": 1,
            "ClientTimeoutUnit": "ms",
            "ListenerPort": 1,
            "EnableSourceIp": "on",
            "EnableRepeaterMode": "on",
            "ServerTimeout": "10000",
            "ConnectTimeoutUnit": "s",
            "BackendServer": [
                {
                    "IP": "",
                    "MaxConn": 2000,
                    "Port": 1,
                    "Weight": "256"
                }
            ],
            "ConnectTimeout": "22",
            "ClientTimeout": "1010",
        }
    ]
    response, err = client.ModifyLoadBalancerStrategys(request)
    print(f"ModifyLoadBalancerStrategys response {response}, err: {err}")


def TestClient_ModifyLoadBalancerName():
    client, err = NewClient(ak, sk, Beijing_region, reqTimeout)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyLoadBalancerNameRequest()
    request.InstanceUuid = ""
    request.InstanceName = 'test'
    response, err = client.ModifyLoadBalancerName(request)
    print(f"ModifyLoadBalancerName response {response}, err: {err}")


if __name__ == '__main__':
    TestClient_DescribeZones()
    # TestClient_DescribeLoadBalancersSpec()
    # TestClient_CreateLoadBalancer()
    # TestClient_DescribeLoadBalancers()
    # TestClient_DescribeLoadBalancersModifySpec()
    # TestClient_ModifyLoadBalancerInstanceSpec()
    # TestClient_DeleteLoadBalancer()
    # TestClient_DescribeCACertificates()
    # TestClient_DescribeCACertificate()
    # TestClient_DeleteCACertificate()
    # TestClient_UploadCACertificate()
    # TestClient_DescribeLoadBalancerStrategys()
    # TestClient_ModifyLoadBalancerStrategys()
    # TestClient_ModifyLoadBalancerName()
