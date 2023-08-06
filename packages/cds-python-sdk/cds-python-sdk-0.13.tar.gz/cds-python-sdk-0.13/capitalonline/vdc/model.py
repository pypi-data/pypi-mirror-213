# -*- coding: utf-8 -*-

class BaseRequest:
    ACTION = ''

    def to_param(self):
        json_data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                json_data[key] = value
        return json_data


class DescVdcRequest(BaseRequest):
    ACTION = 'DescribeVdc'

    def __init__(self, VdcId=None, RegionId=None, PageNumber=None, Keyword=None):
        """
        :param VdcId: The id of the vdc
        :type VdcId: str
        :param RegionId:  The region id of the vdc
        :type RegionId: str
        :param PageNumber: The maximum number of item to return
        :type PageNumber: int
        :param Keyword: The name of the vdc,
        :type Keyword: str
        """

        self.VdcId = VdcId
        self.RegionId = RegionId
        self.PageNumber = PageNumber
        self.Keyword = Keyword


class PublicNetWork(BaseRequest):
    def __init__(self, Name=None, Type=None, BillingMethod=None, Qos=None, IPNum=None,
                 AutoRenew=None, FloatBandwidth=None):
        """
        :param Name: Public network name
        :type Name: str
        :param Type: Public network type
        :type Type: str
        :param BillingMethod: Public network billing method
        :type BillingMethod: str
        :param Qos: 带宽大小
        :type Qos: int
        :param IPNum: ip数量
        :type IPNum: int
        :param AutoRenew: 自动续费
        :type AutoRenew: int
        :param FloatBandwidth: 封顶带宽
        :type FloatBandwidth: int
        """
        self.Name = Name
        self.Type = Type
        self.BillingMethod = BillingMethod
        self.Qos = Qos
        self.IPNum = IPNum
        self.AutoRenew = AutoRenew
        self.FloatBandwidth = FloatBandwidth


class CreateVdcRequest(BaseRequest):
    ACTION = 'CreateVdc'

    def __init__(self, RegionId=None, VdcName=None, PublicNetwork=None):
        """
        :param RegionId: The region id of the vdc
        :type RegionId: str
        :param VdcName: The name of vdc
        :type VdcName: str
        :param PublicNetwork: Public network Setting of vdc
        :type PublicNetwork: PublicNetWork
        """
        self.RegionId = RegionId
        self.VdcName = VdcName
        self.PublicNetwork = PublicNetwork

    def to_param(self):
        json_data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == 'PublicNetwork':
                    value = self.PublicNetwork.to_param()
                    if value:
                        json_data[key] = value
                else:
                    json_data[key] = value
        return json_data


class DeleteVdcRequest(BaseRequest):
    ACTION = 'DeleteVdc'

    def __init__(self, VdcId=None):
        """
        :param VdcId: The id of the vdc
        :type VdcId: str
        """
        self.VdcId = VdcId


class CreatePublicNetworkRequest(BaseRequest):
    ACTION = 'CreatePublicNetwork'

    def __int__(self, VdcId=None, Name=None, Type=None, BillingMethod=None,
                Qos=None, IPNum=None, AutoRenew=None, FloatBandwidth=None):
        """
        :param VdcId: The id of the vdc
        :type VdcId: str
        :param Name: Public network name
        :type Name: str
        :param Type: Public network type
        :type Type: str
        :param BillingMethod: Public network billing method
        :type BillingMethod: str
        :param Qos: 带宽大小
        :type Qos: int
        :param IPNum: ip数量
        :type IPNum: int
        :param AutoRenew: 自动续费
        :type AutoRenew: int
        :param FloatBandwidth: 封顶带宽
        :type FloatBandwidth: int
        """
        self.VdcId = VdcId
        self.Name = Name
        self.Type = Type
        self.BillingMethod = BillingMethod
        self.Qos = Qos
        self.IPNum = IPNum
        self.AutoRenew = AutoRenew
        self.FloatBandwidth = FloatBandwidth


class CreatePrivateNetworkRequest(BaseRequest):
    ACTION = 'CreatePrivateNetwork'

    def __int__(self, VdcId=None, Name=None, Type=None, Address=None, Mask=None):
        """
        :param VdcId: vdc编号
        :type  VdcId: str
        :param Name: 公网名称
        :type Name: str
        :param Type: 公网类型
        :type Type: str
        :param Address: 私网地址
        :type Address: str
        :param Mask: 私网掩码
        :type Mask: str
        """
        self.VdcId = VdcId
        self.Name = Name
        self.Type = Type
        self.Address = Address
        self.Mask = Mask


class ModifyPublicNetworkRequest(BaseRequest):
    ACTION = 'ModifyPublicNetwork'

    def __int__(self, PublicId=None, Qos=None):
        """
        :param PublicId: 公网id
        :type PublicId: str
        :param Qos: 带宽大小
        :type Qos: int
        """
        self.PublicId = PublicId
        self.Qos = Qos


class AddPublicIpRequest(BaseRequest):
    ACTION = 'AddPublicIp'

    def __int__(self, PublicId=None, Number=None):
        """
        :param PublicId: 公网id
        :type PublicId: str
        :param Number: ip数量
        :type Number: int
        """
        self.PublicId = PublicId
        self.Number = Number


class DeletePublicIpRequest(BaseRequest):
    ACTION = 'DeletePublicIp'

    def __int__(self, SegmentId=None):
        """
        :param SegmentId: 公网IP段的id
        :type SegmentId: str
        """
        self.SegmentId = SegmentId


class DeletePublicNetworkRequest(BaseRequest):
    ACTION = 'DeletePublicNetwork'

    def __int__(self, PublicId=None):
        """
        :param PublicId: 公网id
        :type PublicId: str
        """
        self.PublicId = PublicId


class DeletePrivateNetworkRequest(BaseRequest):
    ACTION = 'DeletePrivateNetwork'

    def __int__(self, PrivateId=None):
        """
        :param PrivateId: 公网id
        :type PrivateId: str
        """
        self.PrivateId = PrivateId


class RenewPublicNetworkRequest(BaseRequest):
    ACTION = 'RenewPublicNetwork'

    def __int__(self, PublicId=None, AutoRenew=None):
        """
        :param PublicId: 公网id
        :type PublicId: str
        :param AutoRenew: 自动续费
        :type AutoRenew: int
        """
        self.PublicId = PublicId
        self.AutoRenew = AutoRenew


class ModifyVdcNameRequest(BaseRequest):
    ACTION = 'ModifyVdcName'

    def __int__(self, VdcId=None, VdcName=None):
        """
        :param VdcId: vdc的编号
        :type VdcId: str
        :param VdcName: vdc的名称
        :type VdcName: str
        """
        self.VdcId = VdcId
        self.VdcName = VdcName
