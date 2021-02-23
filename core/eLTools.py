#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
from abc import ABCMeta
from enum import Enum

from ext.jsonVerifyUtils import JsonVerifyUtils
from ext.protocolVerifyUtils import ProtocolUtils
from ext.strVerifyUtils import StrUtils
from util.exceptions import ELError
from util.loadExtPy import CloneExtMoudle


class ResponseVerifyType(Enum):
    #String type
    STR = 1
    #Json type
    JSON = 2
    # user define operate
    USER_DEFINE = 3
    # no data response
    NONE = 5
    PROTOCOL = 4


def get_verify_util(keystr: str, data, valueStr: str, apistatus = "")->ResponseVerifyType:
    """
    analyse the verification command at case template
    :param keystr: yaml sub node verification key
    :param data:
    :param valueStr:  yaml sub node verification value
    :param apistatus: the api protocol layer response code
    :return:
    """
    regJson = ":@@"
    regStr = ":#"
    regUserDefine = ":$$"
    regProtocol = ":%"
    keyinfo = keystr.split(regJson)
    if len(keyinfo) == 2:
        return VerifyDataKey(ResponseVerifyType.JSON, keyinfo[1], valueStr, data)
    keyinfo = keystr.split(regStr)

    if len(keyinfo) == 2:
        return VerifyDataKey(ResponseVerifyType.STR, keyinfo[1],valueStr, data)
    keyinfo = keystr.split(regUserDefine)

    if len(keyinfo) == 2:
        return VerifyDataKey(ResponseVerifyType.USER_DEFINE, keyinfo[1], valueStr, data)
    keyinfo = keystr.split(regProtocol)
    if len(keyinfo) == 2:
        return VerifyDataKey(ResponseVerifyType.PROTOCOL, keyinfo[1],valueStr,apistatus)

    else:
        raise ELError("the template no support the EL key  " + keystr)


class VerifyDataKey():
    def __init__(self,keyType, key,value, data):
        self.keyType = keyType
        self.key = key
        # self.value = tuple(str(value).split(" "))
        self.value = value
        self.data = data

    def verify_cmd(self):
        if self.keyType == ResponseVerifyType.STR:
            # call str verify
            util = StrUtils(self.data)
            util.executeVerify(self.key, self.value.split(" "))


        elif self.keyType == ResponseVerifyType.JSON:
            #  call json verify
            util = JsonVerifyUtils(self.data)
            util.executeVerify(self.key, self.value)

        elif self.keyType == ResponseVerifyType.PROTOCOL:
            #  call api protocol verify
            util = ProtocolUtils(self.data)
            util.executeVerify(self.key, self.value)

        elif self.keyType == ResponseVerifyType.USER_DEFINE:
            #  call ext user define verify
            #  Load user ext file from current dir
            extfilename = "ext_python/ext_class_test.py"
            util = CloneExtMoudle(modulefile=extfilename, class_name="ExtClass" ,apiData=self.data)
            #user extention metion input params offer is api response data.

            util.exec_method(self.key, self.value)

        else:
            raise ELError("the template no support the EL key  " + self.keyType)

    def tearDown(self):
        """
        write execute result to file.
        :return:
        """

        pass


class ELTools(metaclass=ABCMeta):
    """
     pattern usage.
     if found the instance will be use the inject to ELTools Object.

    """
    def __init__(self, key,value,data):
        self.data = data
        self.key = key
        self.value = value

    def execute_verify(self):
        """
        execute the verification command at template
        :return:
        """

        pass