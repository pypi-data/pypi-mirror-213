# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict


class BaseData(object):
    def __init__(self):
        super().__init__()

    def to_params(self):
        value = {}
        value.update(self.__dict__)
        return value


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


class DescribeZonesRequest(BaseRequest):
    {}


class DescribeLoadBalancersSpecRequest(BaseRequest):
    RegionId: str


class CreateLoadBalancerRequest(BaseRequest):
    RegionId: str
    VdcId: str
    BasePipeId: str
    InstanceName: str
    PaasGoodsId: int
    _Ips: []
    Amount: int

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._Ips:
            value['Ips'] = self._Ips
        return value

    @property
    def Ips(self):
        value = []
        for item in self._Ips:
            value.append(item.__dict__)
        return value

    @Ips.setter
    def Ips(self, data: list):
        self._Ips = data


class Ips:
    IsVip: int
    PipeType: str
    PipeId: str
    SegmentId: str


class DescribeLoadBalancersRequest(BaseRequest):
    IP: str
    InstanceUuid: str
    InstanceName: str
    StartTime: str
    EndTime: str


class DescribeLoadBalancersModifySpecRequest(BaseRequest):
    InstanceUuid: str


class ModifyLoadBalancerInstanceSpecRequest(BaseRequest):
    InstanceUuid: str
    PaasGoodsId: int


class DeleteLoadBalancerRequest(BaseRequest):
    InstanceUuid: str


class DescribeCACertificatesRequest(BaseRequest):
    {}


class DescribeCACertificateRequest(BaseRequest):
    CertificateId: str


class DeleteCACertificateRequest(BaseRequest):
    CertificateId: str


class UploadCACertificateRequest(BaseRequest):
    Certificate: str
    PrivateKey: str
    CertificateName: str


class DescribeLoadBalancerStrategysRequest(BaseRequest):
    InstanceUuid: str


class ModifyLoadBalancerStrategysRequest(BaseRequest):
    InstanceUuid: str
    _HttpListeners: []
    _TcpListeners: []

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._HttpListeners:
            value['HttpListeners'] = self._HttpListeners
        if self._TcpListeners:
            value['TcpListeners'] = self._TcpListeners
        return value

    @property
    def HttpListeners(self):
        value = []
        for item in self._HttpListeners:
            value.append(item.__dict__)
        return value

    @HttpListeners.setter
    def HttpListeners(self, data):
        self._HttpListeners = data

    @property
    def TcpListeners(self):
        value = []
        for item in self._TcpListeners:
            value.append(item.__dict__)
        return value

    @TcpListeners.setter
    def TcpListeners(self, data: list):
        self._TcpListeners = data


class HttpListeners:
    ServerTimeoutUnit: str
    ServerTimeout: str
    StickySession: str
    AclWhiteList: list
    _CertificateIds: []
    ListenerMode: str
    MaxConn: int
    ConnectTimeoutUnit: str
    Scheduler: str
    _SessionPersistence: {}
    _BackendServer: []
    ConnectTimeout: str
    ClientTimeout: str
    ListenerName: str
    ClientTimeoutUnit: str
    ListenerPort: int
    _Option: {}

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._CertificateIds:
            value['CertificateIds'] = self._CertificateIds
        if self._SessionPersistence:
            value['SessionPersistence'] = self._SessionPersistence
        if self._BackendServer:
            value['BackendServer'] = self._BackendServer
        if self._Option:
            value['Option'] = self._Option
        return value

    @property
    def CertificateIds(self):
        value = []
        for item in self._CertificateIds:
            value.append(item.__dict__)
        return value

    @CertificateIds.setter
    def CertificateIds(self, data: list):
        self.CertificateIds = data

    @property
    def SessionPersistence(self):
        value = {}
        value.update(self._SessionPersistence.__dict__)
        return value

    @SessionPersistence.setter
    def SessionPersistence(self, session_persistence):
        self.SessionPersistence = session_persistence

    @property
    def BackendServer(self):
        value = []
        for item in self._BackendServer:
            value.append(item.__dict__)
        return value

    @BackendServer.setter
    def BackendServer(self, data: list):
        self.BackendServer = data

    @property
    def Option(self):
        value = {}
        value.update(self._Option.__dict__)
        return value

    @Option.setter
    def Option(self, option):
        self.Option = option


class TcpListeners:
    ServerTimeoutUnit: str
    AclWhiteList: list
    ListenerMode: str
    ListenerName: str
    Scheduler: str
    MaxConn: int
    ClientTimeoutUnit: str
    ListenerPort: int
    ServerTimeout: str
    ConnectTimeoutUnit: str
    _BackendServer: []
    ConnectTimeout: str
    ClientTimeout: str
    EnableSourceIp: str
    EnableRepeaterMode: str

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._BackendServer:
            value['BackendServer'] = self._BackendServer
        return value

    @property
    def BackendServer(self):
        value = []
        for item in self._BackendServer:
            value.append(item.__dict__)
        return value

    @BackendServer.setter
    def BackendServer(self, data: list):
        self._BackendServer = data


class CertificateIds:
    CertificateId: str
    CertificateName: str


class SessionPersistence:
    Key: str
    Mode: int
    _Timer: {}

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._Timer:
            value['Timer'] = self._Timer
        return value

    @property
    def Timer(self):
        value = {}
        value.update(self._Timer.__dict__)
        return value

    @Timer.setter
    def Timer(self, timer):
        self.Timer = timer


class Timer:
    MaxIdle: int
    MaxLife: int


class BackendServer:
    IP: str
    Port: int
    Weight: str
    MaxConn: int


class Option:
    _Httpchk: {}

    def to_params(self):
        value = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int) or isinstance(v, str):
                value.update({k: v})
        if self._Httpchk:
            value['Httpchk'] = self._Httpchk
        return value

    @property
    def Httpchk(self):
        value = {}
        value.update(self._Httpchk.__dict__)
        return value

    @Httpchk.setter
    def Httpchk(self, httpchk):
        self.Httpchk = httpchk


class Httpchk:
    Method: str
    Uri: str


class ModifyLoadBalancerNameRequest(BaseRequest):
    InstanceUuid: str
    InstanceName: str
