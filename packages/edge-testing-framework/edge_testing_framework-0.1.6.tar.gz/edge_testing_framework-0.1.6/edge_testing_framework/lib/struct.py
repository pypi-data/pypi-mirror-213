# coding:utf-8

from ctypes import *

# from enum import Enum


# 每次运行用例前都会覆盖，请勿在此处定义函数

"""
结构体定义: struct.py 中已有结构体可直接调用，如不存在请暂时在 c.py 中定义
调用方式 struct.AlarmRule()  或 c.OtherClass()
"""


def string_buffer(init, size=None):
    """
    对 ctypes 的 create_string_buffer 比较长的方法名精简
    :param init:
    :param size:
    :return:
    """
    return create_string_buffer(init, int(size))


def dimensional_array(dimensional_num, c_type, size1, size2=None, func_x=None, index=0):
    """
    多维数组统一方法: dimensional_array()
    :param dimensional_num: 维度 1、2、3
    :param c_type: 类型
    :param size1: 大小1
    :param size2: 大小2
    :param func_x: 添加到二维数组中的值或函数等, 当 func_x 是列表或元祖时 按顺序添加到多维数组中
    :param index: 默认第一个位置添加
    :return: 一/二维数组

    举例：
    # json{'version': struct.dimensional_array(1, c_char, 128)}  一维数组
    # json{'identifier': struct.dimensional_array(2, c_char, 128, 100, create_string_buffer(b"EDGE_HMI_YC1", int(128)))}  二维数组
    # json={'c_func_name': 'InoAccessHisDatasGet', 'queryInfo.byref':struct.InoAccessQueryInfo(startTime=int(0),endTime=c.localcurtime_to_stamp(),identifier=struct.dimensional_array(2, c_char, 128, 100, create_string_buffer(b"EDGE_HMI_YC1", int(128))))}  结构体嵌套二维数组
    # json={'gam': struct.dimensional_array(2, c_char, 128, 3, (struct.string_buffer(b'aaa', 128), struct.string_buffer(b'bbb', 128), struct.string_buffer(b'ccc', 128)))} # 批量传参, 注意第五个参数func_x 传递的是() 或 []
    """
    if int(dimensional_num) == 1:
        return (c_type * int(size1))()  # 一维数组
    elif int(dimensional_num) == 2:
        char_array = ((c_type * int(size1)) * int(size2))()  # 二维数组
        if type(func_x) in (list, tuple):
            for func_index, func_j in enumerate(func_x):
                char_array[func_index] = func_j
        else:
            char_array[int(index)] = func_x
        return char_array


def array_struct(struct_name, num, *args):
    """
    统一调用: struct.array_struct()
    批量 获取多个 数据结构
    :param struct_name: 结构体名
    :param num: 结构体数量
    :param args: 结构体参数
    :return:

    举例：
    #  json={'c_func_name': 'InoAlmRuleRead', 'alm_obj.byref': struct.AlarmRule(id=b'CNTEST_HCTEST_ALM2')}  # 单条
    #  json={'c_func_name': 'InoAlmRuleAllRead','alms_array': struct.array_struct('AlarmRule',30)  # 无参数的
    #  json={'c_func_name': 'InoAlmRuleAllRead','alms_array': struct.array_struct('AlarmRule',30, {'id':b'CNTEST_HCTEST_ALM2'}, {'id':b'CNTEST_HCTEST_YXALM1'}, {'id':b'CNTEST_HCTEST_YXALM2'}, {'id':b'a'})  # 有指定参数的
    #  json={'c_func_name': 'InoAlmRuleAllRead','alms_array': struct.array_struct('AlarmRule',30, b'CNTEST_HCTEST_ALM2', b"a")  # 无指定参数名 顺序传参，（结构体字段顺序）
    #  json={'c_func_name': 'InoAlmRuleAllRead','alms_array': struct.array_struct('AlarmRule',30, (b'CNTEST_HCTEST_ALM2', b'YXCJ2'), (b"a", b'x'))  # 批量tuple 无指定参数名 顺序传参，（结构体字段顺序）
    #  json={'c_func_name': 'InoAlmRuleAllRead','alms_array': struct.array_struct('AlarmRule',30, [b'CNTEST_HCTEST_ALM2', b'YXCJ2'], [b"a", b'x'])  # 批量list 无指定参数名 顺序传参，（结构体字段顺序）

    """
    alms = []
    for i in range(int(num)):
        if i >= len(args) or len(args) == 0:  # 默认值定义超过了 num
            alms.append(eval('{}()'.format(struct_name)))  # 无参数的 array_struct('struct_name', 3)
            continue
        arg_i = args[i]
        if isinstance(arg_i, dict):  # 有指定参数的 array_struct('struct_name', 30, {'id':b'CNTEST_HCTEST_ALM2'}, {'id':b"a"})
            for key, value in arg_i.items():
                sc = eval('{}({}={})'.format(struct_name, key, value))
                alms.append(sc)
        elif type(arg_i) in (tuple, list):
            alms.append(eval('{}(*{})'.format(struct_name, arg_i)))  # 批量tuple/list 无指定参数名 顺序传参，（结构体字段顺序）
        else:
            alms.append(eval('{}({})'.format(struct_name, arg_i)))  # 无指定参数名 顺序传参，（结构体字段顺序）
    alms_array_ = (eval('{}'.format(struct_name)) * len(alms))(*alms)
    return alms_array_


# 存取服务-客户端访问节点
class InoAccessCliPortInfo(Structure):
    _fields_ = [
        ("ip", c_char * 32),
        ("port", c_int32),
        ("nodeId", c_uint32),
        ("name", c_char * 32),
        ("desc", c_char * 64),
        ("isDefault", c_int32)
    ]


# 存取服务-配置信息
class InoAccessCliConfigInfo(Structure):
    _fields_ = [
        ("proxyMode", c_int32),
        ("hostMode", c_int32),
        ("defaultNodeName", c_char * 32),
        ("nodeCount", c_int32),
        ("nodes", POINTER(InoAccessCliPortInfo))
    ]


# 存取服务-查询信息
class InoAccessQueryInfo(Structure):
    _fields_ = [
        ("type", c_int32),
        ("startTime", c_uint64),
        ("endTime", c_uint64),
        ("count", c_int32),
        ("flag", c_int32),
        ("subType", c_int32),
        ("match", c_char * 512),
        ("identifier", (c_char * 128) * 100)
    ]


# 存取服务-事件信息
class InoAccessEventInfo(Structure):
    _fields_ = [
        ("uuid", c_char * 64),
        ("module", c_uint32),
        ("appearTime", c_uint64),
        ("type", c_int32),
        ("reason", c_int32),
        ("source", c_char * 64),
        ("identifier", c_char * 128),
        ("len", c_uint32),
        ("content", c_char * 512)
    ]


# 存取服务-归档历史数据
class InoAccessHisDataInfo(Structure):
    _fields_ = [
        ("uuid", c_char * 64),
        ("id", c_char * 128),
        ("q", c_uint16),
        ("type", c_uint32),
        ("time", c_uint64),
        ("len", c_uint32),
        ("value", c_char * 32)
    ]


# 存取服务-告警信息
class InoAccessAlarmInfo(Structure):
    _fields_ = [
        ("uuid", c_char * 40),
        ("id", c_char * 128),
        ("oper", c_char * 64),
        ("status", c_uint8),
        ("parm1", c_uint8),
        ("r2", c_uint8),
        ("r3", c_uint8),
        ("appearTime", c_uint64),
        ("disapperTime", c_uint64),
        ("ackTime", c_uint64),
        ("value", c_double),
    ]


# 存取服务-告警规则
class InoAccessAlarmRule(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("tag", c_char * 128),
        ("relativetags", c_char * 512),
        ("desc", c_char * 128),
        ("area", c_char * 64),
        ("deadband", c_double),
        ("value", c_double),
        ("interval", c_uint16),
        ("enable", c_uint8),
        ("autoAck", c_uint8),
        ("condition", c_uint8),
        ("deadbandType", c_uint8),
        ("severity", c_uint8),
        ("comparison", c_uint8),
    ]


# 存取服务-告警确认
class InoAccessAlarmInfoAck(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("oper", c_char * 64),
    ]


# 存取服务-代理中联合体
class DataValue(Union):
    _fields_ = [
        ("bVal", c_bool),
        ("cVal", c_char),
        ("iByte", c_int8),
        ("byte", c_uint8),
        ("iWord", c_int16),
        ("uiWord", c_uint16),
        ("iVal", c_int32),
        ("uiVal", c_uint32),
        ("iIVal", c_int64),
        ("uiIVal", c_uint64),
        ("fVal", c_float),
        ("dVal", c_double),
        ("t", c_uint64),
    ]


# 存取服务-代理模式测点变量
class InoAccessValTag(Structure):
    _fields_ = [
        ("tag_name", c_char * 256),
        ("dataType", c_uint8),
        ("value", DataValue),
        ("pStrBuf", c_char_p),
        ("pStrBufLen", c_int32),
        ("timStamp", c_uint64),
        ("qos", c_uint16),
    ]


# 告警服务-获取告警规则用例
class AlarmRule(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("tag", c_char * 128),
        ("relativetags", c_char * 512),
        ("desc", c_char * 128),
        ("area", c_char * 64),
        ("deadband", c_double),
        ("value", c_double),
        ("interval", c_uint16),
        ("enable", c_uint8),
        ("autoAck", c_uint8),
        ("condition", c_uint8),
        ("deadbandType", c_uint8),
        ("severity", c_uint8),
        ("comparison", c_uint8),
    ]


def alms_array(id1, id2, id3, id4):
    """获取多个告警规则用例 数据结构传值"""
    alms = [
        AlarmRule(id1, b'', b'', b'', b'', 0, 0, 0, 0, 0, 0, 0, 0),
        AlarmRule(id2, b'', b'', b'', b'', 0, 0, 0, 0, 0, 0, 0, 0),
        AlarmRule(id3, b'', b'', b'', b'', 0, 0, 0, 0, 0, 0, 0, 0),
        AlarmRule(id4, b'', b'', b'', b'', 0, 0, 0, 0, 0, 0, 0, 0),
    ]

    alms_array_ = (AlarmRule * len(alms))(*alms)
    return alms_array_


# 告警服务-告警信息获取
class AlarmInfo(Structure):
    """数据结构定义-获取单个直接调用传值"""
    _fields_ = [
        ("uuid", c_char * 40),
        ("id", c_char * 128),
        ("oper", c_char * 64),
        ("status", c_uint8),
        ("parm1", c_uint8),
        ("r2", c_uint8),
        ("r3", c_uint8),
        ("appearTime", c_uint64),
        ("disapperTime", c_uint64),
        ("ackTime", c_uint64),
        ("value", c_double),
    ]


# 告警服务-告警信息确认
class AlarmInfoAck(Structure):
    """数据结构定义-获取单个直接调用传值"""
    _fields_ = [
        ("id", c_char * 128),
        ("oper", c_char * 64)
    ]


# OTA-模块信息
class OtaModInfo(Structure):
    """ota升级模块详细定义"""
    _fields_ = [
        ("code", c_char * 32),
        ("name", c_char * 128),
        ("path", c_char * 256),
        ("version", c_char * 32),
        ("forward", c_int32)
    ]


# OTA-任务信息
class OtaUpgradeTaskInfo(Structure):
    """ota升级任务详细定义"""
    _fields_ = [
        ("code", c_char * 32),
        ("name", c_char * 128),
        ("path", c_char * 256),
        ("version", c_char * 32),
        ("taskId", c_int64),
        ("taskType", c_int32),
        ("taskResult", c_int32),
        ("progress", c_int32),
        ("failMsg", c_char * 256),
        ("operUser", c_char * 128),
        ("updatetime", c_uint64),
        ("pkgName", c_char * 256),
        ("pkgSize", c_int64),
        ("pkgSignMethod", c_char * 32),
        ("pkgSign", c_char * 128),
        ("pkgMd5", c_char * 64),
        ("pkgUrl", c_char * 2048),
        ("pkgType", c_int32),
        ("forward", c_int32)
    ]


# 网关服务-联网信息
class InoGwNortConInfo(Structure):
    _fields_ = [
        ("localIp", c_char * 64),
        ("remoteIp", c_char * 64),
        ("localPort", c_char * 16),
        ("remotePort", c_char * 16),
        ("mqttConStatus", c_int32),
    ]


# 资源同步-同步信息
class InoSyncRespInfo(Structure):
    _fields_ = [
        ("pStrResp", c_char_p),
        ("pdwModCodeArr", c_uint32),
        ("nCodeArrSize", c_uint32),
        ("pStrVerList", c_char_p),
    ]


# 通用服务-公共配置信息
class commonInfo(Structure):
    _fields_ = [
        ("platform", c_char * 64),
        ("product", c_char * 64),
        ("device", c_char * 64),
        ("productKey", c_char * 64),
        ("deviceKey", c_char * 64),
        ("desc", c_char * 64),
        ("version", c_char * 64),
        ("datetime", c_char * 64),
        ("dataPath", c_char * 64),
        ("logPath", c_char * 64),
        ("debuglogPath", c_char * 64),
        ("language", c_char * 64),
    ]


# 通用服务-修改部分系统信息
class partcommonInfo(Structure):
    _fields_ = [
        ("productKey", c_char * 64),
        ("deviceKey", c_char * 64),
    ]


# 鉴权服务 - 用户配置信息
class UserInfo(Structure):
    _fields_ = [
        ("user", c_char_p),
        ("authCode", c_char_p),
        ("password", c_char_p),
    ]


# 日志服务 - 日志信息内容
class LogContent(Structure):
    _fields_ = [
        ("modNo", c_int32),
        ("level", c_int32),
        ("time", c_char * 32),
        ("content", c_char * 128),
    ]


# 事件服务 - 通用事件记录
class eventContent(Structure):
    _fields_ = [
        ("len", c_uint16),
        ("ctx", c_char * 64),
    ]


# 事件服务 - 通用数据结构
class eventItem(Structure):
    _fields_ = [
        ("occurTime", c_uint64),
        ("modCode", c_uint32),
        ("eventType", c_uint8),
        ("ui8Reason", c_uint8),
        ("contentMode", c_uint8),
        ("reserve", c_uint8),
        ("eventSrc", c_char * 64),
        ("index", c_char * 128),
        ("content", eventContent),
    ]


# 事件服务 - 通用数据结构
class eventQueryDBInfo(Structure):
    _fields_ = [
        ("tStart", c_uint64),
        ("tEnd", c_uint64),
        ("eventID", c_uint32),
        ("bTimeFlag", c_bool),
        ("eventType", c_uint8),
        ("index", c_char * 128),
        ("content", c_char * 512),
    ]


# 事件服务 - 事件名称
class eventTypeDBInfo(Structure):
    _fields_ = [
        ("type", c_uint16),
        ("name", c_char * 32),
    ]


# 事件服务 - 告警事件
class eventAlmStatusContent(Structure):
    _fields_ = [
        ("identifier", c_char * 64),
        ("ruleId", c_char * 128),
        ("type", c_uint8),
        ("level", c_uint8),
        ("status", c_uint8),
        ("rocStatus", c_uint8),
        ("appearTime", c_uint64),
        ("disappearTime", c_uint64),
        ("value", c_double),
        ("seqId", c_char * 40),
        ("relative", c_char * 64),
    ]


# 事件服务 - 自检事件
class eventCheckStatusContent(Structure):
    _fields_ = [
        ("nType", c_uint16),
        ("nStatus", c_int16),
    ]


# 归档服务 - 数据信息
class DataInfo(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("type", c_uint32),
        ("q", c_uint16),
        ("reserve", c_uint32),
        ("time", c_uint64),
        ("len", c_uint32),
        ("value", c_char * 32),
        ("txtVal", c_char_p),
    ]


# 归档服务 - 外部数据信息
class ExternDataInfo(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("dataType", c_uint32),
        ("time", c_uint64),
        ("q", c_uint16),
        ("len", c_uint32),
        ("value", c_char * 32),
        ("txtVal", c_char_p),
    ]


# 传输管理 - InoTag信息
class InoTagInfo(Structure):
    _fields_ = [
        ("id", c_char * 64),
        ("deviceId", c_char * 64),
        ("groupName", c_char * 32),
        ("dataBlock", c_char * 64),
        ("dataAddress", c_int32),
        ("addrOffset", c_int32),
        ("byteOrder", c_int32),
        ("dataType", c_int32),
        ("pStrBufLen", c_int32),
        ("rwType", c_int32),
        ("maxValue", c_double),
        ("minValue", c_double),
        ("initValue", c_double),
        ("scale", c_double),
        ("step", c_double),
        ("unit", c_char * 32),
        ("extends", c_char * 128),
        ("userinfo", c_uint8 * 256),
    ]


# 传输管理 - InoDev信息
class InoDevTag(Structure):
    _fields_ = [
        ("id", c_char * 64),
        ("groupName", c_char * 32),
        ("byteOrder", c_int32),
        ("dataType", c_int32),
        ("pValBuf", c_uint8 * 8),
        ("pStrBuf", c_char_p),
        ("pStrBufLen", c_int32),
        ("timStamp", c_uint64),
        ("qos", c_uint16),
        ("userinfo", c_uint8 * 256),
    ]


# 实时服务-数据索引
class txtVal(Structure):
    _fields_ = [
        ("len", c_uint32),
        ("cVal", c_char_p),
    ]


# 实时服务-联合体
class val(Union):
    _fields_ = [
        ("bVal", c_bool),
        ("cVal", c_char),
        ("iByte", c_int8),
        ("byte", c_uint8),
        ("iWord", c_int16),
        ("uiWord", c_uint16),
        ("iVal", c_int32),
        ("uiVal", c_uint32),
        ("iIVal", c_int64),
        ("uiIVal", c_uint64),
        ("fVal", c_float),
        ("dVal", c_double),
        ("t", c_uint64),
        ("tVal", txtVal),
    ]


# 实时服务-数值
class rtdbDataValue(Structure):
    _fields_ = [
        ("dataType", c_uint8),
        ("va", val),
    ]


# 实时服务-数据索引
class rtdbStrIndex(Structure):
    _fields_ = [
        ("id", c_char_p),
        ("len", c_uint32)
    ]


# 实时服务-rtdbDataTag
class rtdbDataTag(Structure):
    _fields_ = [
        ("t", c_uint64),
        ("q", c_uint16),
        ("val", rtdbDataValue),
    ]


# 实时服务-CmdLitetag
class rtdbCmdLiteTag(Structure):
    _fields_ = [
        ("len", c_uint32),
        ("index", c_char * 128),
        ("uuid", c_char * 64),
        ("act", c_uint32),
        ("direction", c_uint32),
        ("result", c_uint16),
        ("ctlVal", rtdbDataValue),
    ]


# 时间结构体
class DatetimeStruct(Structure):
    _fields_ = [
        ("milliSec", c_uint16),
        ("sec", c_uint16),
        ("minute", c_uint16),
        ("hour", c_uint16),
        ("day", c_uint16),
        ("month", c_uint16),
        ("year", c_uint16),
    ]


class InoMqttModCfgUpdateInfo(Structure):
    """配置更新模块详细信息"""
    fields = [
        ("modCode", c_uint32),
        ("updateMode", c_uint32)
    ]