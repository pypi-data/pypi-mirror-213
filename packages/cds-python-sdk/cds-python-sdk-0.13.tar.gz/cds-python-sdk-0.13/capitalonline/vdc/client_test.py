# -*- coding: utf-8 -*-

from capitalonline.common import credential
from capitalonline.common.profile import client_profile, http_profile
from capitalonline.vdc.client import NewClient
from capitalonline.vdc.model import *

secret_id = ''
secret_key = ''


def TestClient_DescribeVdc():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = DescVdcRequest()
    request.VdcId = ''
    request.RegionId = 'CN_Beijing_A'
    # request.Keyword = 'vdc'
    request.PageNumber = 1

    response, err = client.DescribeVdc(request)
    if err:
        print('err:', err.Code)
    else:
        print("Describe Vdc Response: ", response)


def TestClient_CreateVdc():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = CreateVdcRequest()
    request.RegionId = 'CN_Beijing_A'
    request.VdcName = 'test_create_vdc'
    request.PublicNetwork = PublicNetWork(IPNum=8, Qos=10, Name='network name',
                                          BillingMethod='Bandwidth',
                                          Type='Bandwidth_Multi_ISP_BGP',
                                          FloatBandwidth=200)
    response, err = client.CreateVdc(request)
    if err:
        print("err: ", err)
    else:
        print("Create Vdc Response: ", response)


def TestClient_DeleteVdc():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = DeleteVdcRequest()
    request.VdcId = ''
    response, err = client.DeleteVdc(request)
    if err:
        print('err: ', err)
    else:
        print("Delete Vdc Response: ", response)


def TestClient_CreatePublicNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = CreatePublicNetworkRequest()
    request.VdcId = ''
    request.Name = 'name'
    request.Type = 'Bandwidth_Multi_ISP_BGP'
    request.BillingMethod = 'Bandwidth'
    request.Qos = 10
    request.IPNum = 4
    request.AutoRenew = 0
    # request.FloatBandwidth = 200
    response, err = client.CreatePublicNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Create Public Network Response: ', response)


def TestClient_CreatePrivateNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = CreatePrivateNetworkRequest()
    request.VdcId = ''
    request.Name = 'name'
    request.Type = 'manual'
    request.Address = '192.168.255.0'
    request.Mask = 24
    response, err = client.CreatePrivateNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Create Private Network: ', response)


def TestClient_ModifyPublicNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = ModifyPublicNetworkRequest()
    request.PublicId = ''
    request.Qos = 10
    # request.Qos = 30
    response, err = client.ModifyPublicNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Modify Public Network Response: ', response)


def TestClient_AddPublicIp():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = AddPublicIpRequest()
    request.PublicId = ''
    # request.Number = 4
    request.Number = 8
    response, err = client.AddPublicIp(request)
    if err:
        print("err: ", err)
    else:
        print('Add Public Ip Response: ', response)


def TestClient_DeletePublicIp():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = DeletePublicIpRequest()
    # request.SegmentId = 'segment id'
    request.SegmentId = ''
    response, err = client.DeletePublicIp(request)
    if err:
        print('err: ', err)
    else:
        print('Delete Public Ip Response: ', response)


def TestClient_DeletePublicNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = DeletePublicNetworkRequest()
    request.PublicId = ""
    response, err = client.DeletePublicNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Delete Public Network Response: ', response)


def TestClient_DeletePrivateNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = DeletePrivateNetworkRequest()
    request.PrivateId = ""
    response, err = client.DeletePrivateNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Delete Private Network Response: ', response)


def TestClient_RenewPublicNetwork():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = RenewPublicNetworkRequest()
    request.PublicId = ""
    request.AutoRenew = 0
    # request.AutoRenew = 1
    response, err = client.RenewPublicNetwork(request)
    if err:
        print('err: ', err)
    else:
        print('Renew Public Network Response: ', response)


def TestClient_ModifyVdcName():
    client = NewClient(secret_id=secret_id, secret_key=secret_key,
                       region='CN_Beijing_A')
    request = ModifyVdcNameRequest()
    request.VdcId = ''
    request.VdcName = 'test_create_vdc'
    response, err = client.ModifyVdcName(request)
    if err:
        print('err: ', err)
    else:
        print("Modify Vdc Name Response: ", response)


if __name__ == '__main__':
    TestClient_DescribeVdc()
    # TestClient_CreateVdc()
    # TestClient_DeleteVdc()
    # TestClient_CreatePublicNetwork()
    # TestClient_CreatePrivateNetwork()
    # TestClient_DeletePublicNetwork()
    # TestClient_DeletePrivateNetwork()
    # TestClient_ModifyPublicNetwork()
    # TestClient_AddPublicIp()
    # TestClient_DeletePublicIp()
    # TestClient_RenewPublicNetwork()
    # TestClient_ModifyVdcName()
