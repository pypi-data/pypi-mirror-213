# -*- coding: utf-8 -*-

from capitalonline.instance.client import NewClient, NewAddInstanceRequest, NewModifyInstanceNameRequest, \
    NewDescribeInstanceRequest, NewDeleteInstanceRequest, NewModifyInstanceSpecRequest, NewCreateDiskRequest, \
    NewResizeDiskRequest, NewDeleteDiskRequest, NewStartInstancesRequest, NewStopInstancesRequest, \
    NewRebootInstancesRequest, NewModifyIpRequest, NewExtendSystemDiskRequest, NewResetInstancesPasswordRequest, \
    NewResetImageRequest, NewModifyInstanceChargeTypeRequest
from capitalonline.instance.models import DataDisk, PrivateIp, SystemDisk, OrderedIP

ak = ''
sk = ''
Beijing_region = 'Beijing'


def TestClient_CreateInstance():
    """
    Test create a new instance.
    :return:
    """
    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewAddInstanceRequest()
    request.RegionId = 'CN_Shanghai_C'                     #region id must be set.
    request.VdcId = ''                                     #vdc id must be set.
    request.Password = ''                                  #password must be set.
    request.InstanceName = 'test1'                         #instance name must be set.
    request.InstanceChargeType = 'PostPaid'
    request.AutoRenew = 0
    request.Cpu = 4                                        #cpu must be set.
    request.Ram = 4                                        #ram must be set.
    request.ImageId = 'Centos_7.6_64'
    request.PublicIp = ['auto']
    request.InstanceType = 'CCS.IC3V2'                     #instance type must be set.
    request.UTC = False

    dd1 = DataDisk()
    dd1.Size = 200
    dd1.Type = 'high_disk'

    ip1 = PrivateIp()
    ip1.PrivateId = ''                                     #if set private ip, private id must be set.
    ip1.IP = ['auto']

    request.DataDisks = [dd1]
    request.PrivateIp = [ip1]

    ordered_ip1 = OrderedIP()                              # if set ordered ip, pipe id must be set. And if this parameter is used, other parameters(such as PublicIp OR PrivateIp) do not take effect.
    ordered_ip1.PipeId = ''
    ordered_ip1.IP = ['auto']

    ordered_ip2 = OrderedIP()
    ordered_ip2.PipeId = ''
    ordered_ip2.IP = ['auto']

    request.OrderedIP = [ordered_ip1] + [ordered_ip2]

    system_disk = SystemDisk()
    system_disk.IOPS = 5
    system_disk.Size = 20
    system_disk.Type = 'ssd_system_disk'

    request.SystemDisk = system_disk
    resp, err = client.CreateInstance(request)
    print(f'Create instance response:{resp}, err:{err}')


def TestClient_DescribeInstance():
    """
    :return: instance information
    """
    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewDescribeInstanceRequest()
    request.VdcId = ""
    request.PageNumber = 1
    request.PageSize = 1000
    request.InstanceId = ""
    request.PublicIp = []
    response, err = client.DescribeInstance(request)
    print(f"Describe instance response {response}, err: {err}")


def TestClient_ModifyInstanceName():
    """
    Modify instance name.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyInstanceNameRequest()
    request.InstanceId = "instance id"                                        #instance id must be set
    request.InstanceName = "new_instance_name"                                #instance name must be set.
    response, err = client.ModifyInstanceName(request)
    print(f"Modify instance name response: {response}, err: {err}")


def TestClient_DeleteInstance():
    """
    Delete some instances.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewDeleteInstanceRequest()
    request.InstanceIds = ["instance_id1,instance_id2"]                      #instance id must be set.
    response, err = client.DeleteInstance(request)
    print(f"Delete instance response: {response}, err:{err}")


def TestClient_ModifyInstanceSpec():
    """
    Modify the instance spec.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyInstanceSpecRequest()
    request.InstanceId = "instance_id"                              #instance id must be set.
    request.Ram = 8
    request.Cpu = 4
    response, err = client.ModifyInstanceSpec(request)
    print(f"Modify instance spec response:{response}, err:{err}")


def TestClient_CreateDisk():
    """
    Create a disk for instance.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewCreateDiskRequest()
    request.InstanceId = "instance id"                                             #instance id must be set.
    disk = DataDisk()
    disk.Size = 20
    disk.IOPS = 5
    disk.Type = "ssd_disk"
    request.DataDisks = [disk]
    response, err = client.CreateDisk(request)
    print(f"Create disk response: {response}, err:{err}")


def TestClient_ResizeDisk():
    """
    Resize a instance disk.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewResizeDiskRequest()
    request.InstanceId = "instance_id"                         #instance id must be set.
    request.DiskId = "disk_id"                                 #disk id must be set.
    request.DataSize = 30
    response, err = client.ResizeDisk(request)
    print(f"Resize disk response:{response}, err:{err}")


def TestClient_DeleteDisk():
    """
    Delete a instance disk.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewDeleteDiskRequest()
    request.InstanceId = "instance id"                                  #instance id must be set.
    request.DiskIds = ["disk id"]                                       #disk id must be set.
    response, err = client.DeleteDisk(request)
    print(f"Delete disk response {response}, err:{err}")


def TestClient_StartInstances():
    """
    Start  instance.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewStartInstancesRequest()
    request.InstanceIds = "instance_id1,instance_id2"                      #instance id must be set.
    response, err = client.StartInstances(request)
    print(f"Start instance Response:{response}, err:{err}")


def TestClient_StopInstances():
    """
    Stop instance.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewStopInstancesRequest()
    request.InstanceIds = "instance_id1,instance_id2"                                #instance id must be set.
    response, err = client.StopInstances(request)
    print(f"Stop instance response:{response}, err:{err}")


def TestClient_RebootInstances():
    """
    Reboot instance.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewRebootInstancesRequest()
    request.InstanceIds = "instance_id1,instance_id2"                         #instance id must be set.
    response, err = client.RebootInstances(request)
    print(f"Reboot instance response:{response}, err:{err}")


def TestClient_ModifyIpAddress():
    """
    Modify instance IP address.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return

    request = NewModifyIpRequest()
    request.InstanceId = "instance_id"                                       #instance id must be set.
    request.InterfaceId = "interface id"                                     #interface id must be set.
    request.Address = "xx.xx.xx.xx"                                          #IP address must be set.
    request.Password = "xxxx"                                                #Instance's Password must be set.
    response, err = client.ModifyIpAddress(request)
    print(f"Modify instance IP response:{response}, err:{err}")


def TestClient_ExtendSystemDisk():
    """
    Extend system disk of instance.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewExtendSystemDiskRequest()
    request.InstanceId = "instance_id"                                      #instance id must be set.
    request.Size = 30                                                       #optional
    request.IOPS = 10                                                       #optional
    response, err = client.ExtendSystemDisk(request)
    print(f"Extend system disk response:{response}, err:{err}")


def TestClient_ResetInstancesPassword():
    """
    Reset instance password
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewResetInstancesPasswordRequest()
    request.InstanceIds = "instance id"                                            #instance id must be set.
    request.Password = "xxxxxx"                                                    #Password must be set.
    response, err = client.ResetInstancesPassword(request)
    print(f"Reset Instances Password response:{response}, err:{err}")


def TestClient_ResetImage():
    """
    Reset instance image.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewResetImageRequest()
    request.InstanceId = "instance id"                                      #Instance id must be set.
    request.ImageId = "image id"                                            #Image id must be set.
    request.Password = 'xxxxxxx'                                            #Instnace password must be set.
    response, err = client.ResetImage(request)
    print(f"Reset Instances Password response:{response}, err:{err}")


def TestClient_ModifyInstanceChargeType():
    """
    Modify instance charge type to postpaid or prepaid.
    :return:
    """

    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'err:{err}')
        return
    request = NewModifyInstanceChargeTypeRequest()
    request.InstanceId = "instance id"                                           #Instance id must be set.
    request.InstanceChargeType = 'PrePaid'                                       #Charge type must be set
    response, err = client.ModifyInstanceChargeType(request)
    print(f"Modify Instance Charge Type response:{response}, err:{err}")


if __name__ == '__main__':
    # TestClient_CreateInstance()
    # TestClient_DescribeInstance()
    # TestClient_ModifyInstanceName()
    # TestClient_ModifyInstanceSpec()
    # TestClient_CreateDisk()
    # TestClient_ResizeDisk()
    # TestClient_DeleteDisk()
    # TestClient_StopInstances()
    # TestClient_StartInstances()
    # TestClient_RebootInstances()
    # TestClient_DeleteInstance()
    # TestClient_ModifyIpAddress()
    # TestClient_ExtendSystemDisk()
    # TestClient_ResetInstancesPassword()
    # TestClient_ResetImage()
    TestClient_ModifyInstanceChargeType()




