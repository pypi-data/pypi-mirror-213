# -*- coding: utf-8 -*-

class BaseRequest:
    service: str
    version: str
    action: str

    def __init__(self, service, version, action):
        super().__init__()
        self.service = service
        self.version = version
        self.action = action

    def to_params(self):
        value = {}
        value.update(self.__dict__)
        return value


class AddInstanceRequest(BaseRequest):
    RegionId: str
    VdcId: str
    InstanceName: str
    InstanceChargeType: str
    Password: str
    PublicKey: str
    Cpu: str
    Ram: str
    InstanceType: str
    ImageId: str
    AssignCCSId: str
    _SystemDisk: {}
    _DataDisks = []
    _PrivateIp = []
    AutoRenew: int
    PrepaidMonth: int
    _PublicIp = []
    Amount: int
    UTC: int
    ImagePassword: str
    _UserData = []
    # 自定义排序网卡
    _OrderedIP = []

    def __init__(self, service, version, action):
        super().__init__(service, version, action)

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._DataDisks:
            value['DataDisks'] = self.DataDisks
        if self._PrivateIp:
            value['PrivateIp'] = self.PrivateIp
        if self._SystemDisk:
            value['SystemDisk'] = self.SystemDisk
        if self._PublicIp:
            value['PublicIp'] = self.PublicIp
        if self._UserData:
            value['UserData'] = self.UserData
        if self._OrderedIP:
            value['OrderedIP'] = self.OrderedIP
        return value

    @property
    def DataDisks(self):
        value = []
        for item in self._DataDisks:
            value.append(item.__dict__)
        return value

    @DataDisks.setter
    def DataDisks(self, data: list):    
        self._DataDisks = data

    @property
    def PrivateIp(self):
        value = []
        for item in self._PrivateIp:
            value.append(item.__dict__)
        return value

    @PrivateIp.setter
    def PrivateIp(self, private_ip):
        self._PrivateIp = private_ip

    @property
    def SystemDisk(self):
        value = {}
        value.update(self._SystemDisk.__dict__)
        return value

    @SystemDisk.setter
    def SystemDisk(self, system_disk):
        self._SystemDisk = system_disk

    @property
    def PublicIp(self):
        return self._PublicIp

    @PublicIp.setter
    def PublicIp(self, public_ip):
        self._PublicIp = public_ip

    @property
    def UserData(self):
        value = []
        for item in self._UserData:
            value.append(item.__dict__)
        return value

    @UserData.setter
    def UserData(self, user_data):
        self._UserData = user_data

    @property
    def OrderedIP(self):
        value = []
        for item in self._OrderedIP:
            value.append(item.__dict__)
        return value

    @OrderedIP.setter
    def OrderedIP(self, ordered_ips):
        self._OrderedIP = ordered_ips


class SystemDisk:
    Type: str
    IOPS: int
    Size: int


class DataDisk:
    Size: int
    Type: str
    IOPS: int


class PrivateIp:
    PrivateId: str
    IP: list


class OrderedIP:
    PipeId: str
    IP: list


class DescribeInstanceRequest(BaseRequest):
    VdcId: str
    InstanceId: str
    PublicIp: list
    PageNumber: int
    PageSize: int


class DeleteInstanceRequest(BaseRequest):
    InstanceIds: list


class ModifyInstanceNameRequest(BaseRequest):
    InstanceId: str
    InstanceName: str


class ModifyInstanceSpecRequest(BaseRequest):
    InstanceId: str
    Cpu: int
    Ram: int
    InstanceType: str


class CreateDiskRequest(BaseRequest):
    InstanceId: str
    _DataDisks = []

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._DataDisks:
            value['DataDisks'] = self.DataDisks
        return value

    @property
    def DataDisks(self):
        value = []
        for item in self._DataDisks:
            value.append(item.__dict__)
        return value

    @DataDisks.setter
    def DataDisks(self, data: list):
        self._DataDisks = data


class ResizeDiskRequest(BaseRequest):
    InstanceId: str
    DiskId: str
    DataSize: int
    IOPS: int


class DeleteDiskRequest(BaseRequest):
    InstanceId: str
    DiskIds: list


class ModifyIpRequest(BaseRequest):
    InstanceId: str
    InterfaceId: str
    Address: str
    Password: str


class ExtendSystemDiskRequest(BaseRequest):
    InstanceId: str
    Size: int
    IOPS: int


class ResetInstancesPasswordRequest(BaseRequest):
    InstanceIds: str
    Password: str


class ResetImageRequest(BaseRequest):
    InstanceId: str
    ImageId: str
    ImagePassword: str
    Password: str
    PublicKey: str
    ProductId: str
    _UserData = []

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._UserData:
            value['UserData'] = self.UserData
        return value

    @property
    def UserData(self):
        value = []
        for item in self._UserData:
            value.append(item.__dict__)
        return value

    @UserData.setter
    def UserData(self, user_data):
        self._UserData = user_data


class ModifyInstanceChargeTypeRequest(BaseRequest):
    InstanceId: str
    InstanceChargeType: str
    AutoRenew: str
    PrepaidMonth: str


class StopInstanceRequest(BaseRequest):
    InstanceId: str


class RebootInstanceRequest(BaseRequest):
    InstanceId: str


class StartInstanceRequest(BaseRequest):
    InstanceId: str


class StartInstancesRequest(BaseRequest):
    InstanceIds: str


class StopInstancesRequest(BaseRequest):
    InstanceIds: str


class RebootInstancesRequest(BaseRequest):
    InstanceIds: str
