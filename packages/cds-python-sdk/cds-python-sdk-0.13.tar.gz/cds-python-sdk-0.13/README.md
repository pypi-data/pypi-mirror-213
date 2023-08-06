English|[简体中文](README-CN.md)

<p align="center">
<a href=" https://www.alibabacloud.com"><img src="https://www.capitalonline.net/templets/default/icon/logo_header.png"></a>
</p>


<h1 align="center">CapitalOnline Cloud SDK for python</h1>

The project aim to build a python SDK for [CapitalOnline](https://www.capitalonline.net)  Cloud Platform, which help users to access CapitalOnline Cloud Service such as GIC, GBS, GPN and manage the resource easily.

It is based on the official  [Open API](https://github.com/capitalonline/openapi/blob/master/README.md).

# Features

You can find all the available actions from [here](https://github.com/capitalonline/openapi/blob/master/%E9%A6%96%E4%BA%91OpenAPI(v1.2).md). List some of them below:

- [x] Instance Management
  - [x] CreateInstance
  - [x] DescribeInstance
  - [x] DeleteInstance
  - [x] ModifyInstanceName
  - [x] ModifyInstanceSpec
  - [x] CreateDisk
  - [x] ResizeDisk
  - [x] DeleteDisk
  - [x] ModifyIpAddress
  - [x] ExtendSystemDisk
  - [x] ResetInstancesPassword
  - [x] ResetImage
  - [x] ModifyInstanceChargeType
  - [x] StartInstance
  - [x] StartInstances
  - [x] StopInstances
  - [x] RebootInstances

- [x] Vdc Management
  - [x] DescribeVdc
  - [x] CreateVdc
  - [x] DeleteVdc
  - [x] CreatePublicNetwork
  - [x] CreatePrivateNetwork
  - [x] ModifyPublicNetwork
  - [x] AddPublicIp
  - [x] DeletePublicIp
  - [x] DeletePublicNetwork
  - [x] DeletePrivateNetwork
  - [x] RenewPublicNetwork
  - [x] ModifyVdcName
  
 - [x] HaProxy Management
    - [x] DescribeZones
    - [x] DescribeLoadBalancersSpec
    - [x] CreateLoadBalancer
    - [x] DescribeLoadBalancers
    - [x] DescribeLoadBalancersModifySpec
    - [x] ModifyLoadBalancerInstanceSpec
    - [x] DeleteLoadBalancer
    - [x] DescribeCACertificates
    - [x] DescribeCACertificate
    - [x] DeleteCACertificate
    - [x] UploadCACertificate
    - [x] DescribeLoadBalancerStrategys
    - [x] ModifyLoadBalancerStrategys
    - [x] ModifyLoadBalancerName

# Installation

```shell
# git clone https://github.com/capitalonline/cds-python-sdk.git
# cd cds-python-sdk
# python setup.py install
```

# Examples

```python
#!/usr/bin/python
from capitalonline.instance.client import NewClient,NewAddInstanceRequest
from capitalonline.instance.models import DataDisk, PrivateIp, SystemDisk, OrderedIP
ak = ''
sk = ''
Beijing_region = 'Beijing'

def TestClient_CreateInstance():
    # Init a credential with Access Key Id and Secret Access Key
    # You can apply them from the CDS web portal
    #init a client
    client, err = NewClient(ak, sk, Beijing_region)
    if err:
        print(f'API request failed,err:{err}')
        return
    #init instance data
    request = NewAddInstanceRequest()
    request.RegionId = 'CN_Shanghai_C'         #region id must be set.
    request.VdcId = ''                         #vdc id must be set.
    request.Password = '********'              #password must be set.
    request.InstanceName = 'test1'             #instance name must be set.
    request.InstanceChargeType = 'PostPaid'
    request.AutoRenew = 0
    request.Cpu = 4                            #cpu must be set.
    request.Ram = 4                            #ram must be set.
    request.ImageId = 'Centos_7.6_64'
    request.PublicIp = ['auto']
    request.InstanceType = 'CCS.IC3V2'         #instance type must be set.
    request.UTC = False

    dd1 = DataDisk()
    dd1.Size = 200
    dd1.Type = 'high_disk'

    ip1 = PrivateIp()
    ip1.PrivateId = ''                         #if set private ip, private id must be set.
    ip1.IP = ['auto']

    request.DataDisks = [dd1]
    request.PrivateIp = [ip1]
    
    ordered_ip1 = OrderedIP()                  # if set ordered ip, pipe id must be set. And if this parameter is used, other parameters(such as PublicIp OR PrivateIp) do not take effect.
    ordered_ip1.PipeId = ''
    ordered_ip1.IP = ['auto']

    request.OrderedIP = [ordered_ip1]

    system_disk = SystemDisk()
    system_disk.IOPS = 5
    system_disk.Size = 20
    system_disk.Type = 'ssd_system_disk'

    request.SystemDisk = system_disk
    # send request get response.
    resp, err = client.CreateInstance(request)    
    print(f'Create instance response:{resp}, err:{err}')
    
if __name__ == '__main__':
    TestClient_CreateInstance()
```

## Contributing

We work hard to provide a high-quality and useful SDK for CapitalOnline Cloud, and we greatly value feedback and contributions from our community. Please submit your issues or pull requests through GitHub.

## References

- [CDS OpenAPI Explorer](https://github.com/capitalonline/openapi)

## License

[Apache License v2.0](./LICENSE)