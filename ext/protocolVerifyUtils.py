#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
from abc import ABCMeta

from util.exceptions import ELError


class ProtocolUtils(metaclass= ABCMeta):
    def __init__(self, code):
        self.statusCode = str(code)

    def status(self,el):
        #expect_status = str(el).replace(","," ").split(" ")
        if self.statusCode in el:
            pass
        else:
            assert False, "{0} actual response code not in {1}".format(self.statusCode, el)




    def executeVerify(self,ELKey, *args):
        if hasattr(ProtocolUtils, ELKey):
            method = getattr(self, ELKey)
            return method(*args)
        else:
            raise ELError("protocal hook method : " + ELKey + " not found.")

