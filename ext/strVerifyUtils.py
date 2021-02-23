#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
from abc import ABCMeta

from util.exceptions import ELError


class StrUtils(metaclass= ABCMeta):
    def __init__(self,src_str):
        self._src_str: str = src_str
    def len(self, operator,value_diff):
        strlen = len(self._src_str)
        value = int(value_diff)
        #print(value)
        if operator == '=' or operator == 'eq':
            assert strlen == value, "verified the string len fail. src len is : " + str(strlen) + " not equal "+ str(value)
        elif operator == '>' or operator == 'gt':
            assert strlen > value, "verified the string len fail. src len is : " + str(strlen) + " not great " + str(value)
        elif operator == '>=' or operator == 'ge':
            assert strlen >= value, "verified the string len fail. src len is : " + str(strlen) + " not great or equal" + str(value)
        elif operator == '<' or operator == 'lt':
            assert strlen < value, "verified the string len fail. src len is : " + str(strlen) + " not less " + str(value)
        elif operator == '<=' or operator == 'le':
            assert strlen <= value, "verified the string len fail. src len is : " + str(strlen) + " not less or equal" + str(value)
        elif operator == '!=' or operator == 'ne':
            assert strlen != value, "verified the string len fail. src len is : " + str(strlen) + "  equal" + str(value)


    def strContain(self,substr):
        assert self._src_str.__contains__(substr), "verified strcontain fail. " + self._src_str + "  \n do not contain : " + substr

    def strStartwith(self,prefix, start=None, end=None):
        #print(prefix)
        assert self._src_str.startswith(prefix, start, end), "verified strStartwith fail. " + self._src_str + "  \n do not startwith : " + prefix

    def strEndwith(self,suffix, start=None, end=None):
        assert self._src_str.endswith(suffix, start, end), "verified strStartwith fail. " + self._src_str + "  \n do not startwith : " + suffix

    def executeVerify(self,ELKey, *args):
        if hasattr(StrUtils, ELKey):
            method = getattr(self, ELKey)
            return method(*args)
        else:
            raise ELError("user defined hook method : " + ELKey + " not found.")
    def executeVerify(self,ELKey, args):
        if hasattr(StrUtils, ELKey):
            method = getattr(self, ELKey)
            return method(*args)
        else:
            raise ELError("user defined hook method : " + ELKey + " not found.")

if __name__ == '__main__':
    response = "hello wuage."
    util = StrUtils(response)
    # print(util.strStartwith("hello"))
    #util.executeVerify("strStartwith","hello")
    elvalue = "gt 0"
    params =elvalue.split(" ")
    print(params)


    util.executeVerify("len", params)
