#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import traceback
from abc import ABCMeta

from core.eLTools import get_verify_util
from util import exceptions, HttpTools

from util.loadConfig import load_file
from util import logger
supportProtocols = ["http", "https"]
class APIRequest():
    """
    the API base data and default verification.
    """
    def getAPIType(self, content):
        if content["types"] not in supportProtocols:
            raise exceptions.MetaCaseFormatFailure("metacase type : " + content["types"] + " don't support")
        else:
            return content["types"]
    def geturl(self,content):
        if content["request"] is None:
            raise exceptions.MetaCaseFormatFailure("metacase request  : " + ["request"]+ " is None")
        if content["request"]["uri"] is None:
            raise exceptions.MetaCaseFormatFailure("metacase request address : " + ["request"]["uri"] + " is None")
        else:
            return content["request"]["uri"]
    def getRequestMethod(self,content):
        if content["request"]["method"] is None:
            raise exceptions.MetaCaseFormatFailure("metacase request method : " + ["request"]["method"] + " is None")
        else:
            return content["request"]["method"]
    def getRequestHeaders(self,content):
        return content["request"]["headers"]
    def getRequestParams(self,content):
        return content["request"]["parms"]
    def getBaseVerifications(self,content):
        return content["request"]["verifications"]
    def __init__(self,content):
        self.type = self.getAPIType(content)
        self.url = self.geturl(content)
        self.method = self.getRequestMethod(content)
        self.headers = self.getRequestHeaders(content)
        self.params = self.getRequestParams(content)
        self.baseVerification = self.getBaseVerifications(content)

    def __repr__(self):
        return "Meta case request data : \n"\
               +" type: "+ str(self.type)\
               + "url:"+str(self.url) +"\n" \
               + "method:" + str(self.method) + "\n" \
               + "headers:"+str(self.headers) +"\n" \
               + "parms:" + str(self.params) + "\n"\
               + "baseVerification:" + str(self.baseVerification) + "\n"
            #current the api support protocols, first version only http[s]

class MetaCase(metaclass = ABCMeta):

    """
    meta testcase template data
    """

    def getCaseName(self,content):
        if content["caseName"] is None:
            raise exceptions.MetaCaseFormatFailure("metacase must define caseName ")
        else:
            return content["caseName"]

    def getParams(self,content):
        return content["parms"]
    def getHeads(self,content):
        try:
            #logger.log_info("metacase header is : " + str(content["headers"]))
            return content["headers"]
        #If no exist then set none
        except (AttributeError,Exception):
            return None
    def getVerifications(self,request: APIRequest, content):
        if content["verifications"] is None:
            if request.baseVerification is not None:
                return request.baseVerification
            else:
                raise exceptions.MetaCaseFormatFailure("metacase must define verification ")
        else:
            return content["verifications"]
    def __init__(self, request: APIRequest, caseInfo):
        """
            :caseInfo is user config in matacase script
            :request is user define the test api detail and default params values.
            If user don't define the value at caseInfo instead from request giving.[Condition- must define value.]
        """
        if caseInfo is not None:
            self.caseName = self.getCaseName(caseInfo)
            self.params = self.getParams(caseInfo)
            self.headers =  self.getHeads(caseInfo)
            self.verifications = self.getVerifications(request, caseInfo)
        else:
            #if not define the case at template the case name use url instead.
            self.caseName = request.url
            self.params = request.params
            self.headers = request.headers
            self.verifications = request.baseVerification
        self.apiType = request.type
        self.uri = request.url
        #
        self.response_code = 0
        # if str(request.getAPIType()).lower().startswith("http"):
        #
        #     self.response = None
        # else:
        #     logger.log_error("API type : " + request.getAPIType() + " current not support."t)
        self.response = ""
        #todo load the local value from template.
        self.local_values = {}
        # todo load the global value from template.
        self.global_values = {}
        #self.global_values.items()


    def call_api(self):
        #only support http or https
        if self.apiType in supportProtocols:
            url = self.apiType + "://" + self.uri

            self.response, self.response_code = HttpTools.request(url, postData=self.params, headers=self.headers)
            logger.log_info("API response data: {0}".format(self.response))

        else:
            logger.log_error("no support API type.")

    def write_exec_report(self,caseName,result, failInfos):
        """
        write execution result to json file. then generate testing report.
        :param caseName:
        :param result:
        :param failInfos:
        :return:
        """
        pass

    def execute_verify(self):
        #excute API the get the response data.
        self.call_api()

        for el_key, el_value in self.verifications.items():
            # execute el
            logger.log_info(" execute verify: " + str(el_key) + ": " + str(el_value))
            try:
                verify_tool = get_verify_util(el_key,self.response,el_value, self.response_code)
                verify_tool.verify_cmd()
            except Exception:
                formatted_lines = traceback.format_exc().splitlines()
                raise "execute verify: {0} : {1}".format(el_key, formatted_lines)



            #todo generate testing report

        #todo push fail message

        #todo write report json file

        #


    def __repr__(self):
        return "Meta case data : \n"\
               +"caseName: "+ self.caseName +"\n" \
               + "headers:"+str(self.headers) +"\n" \
               + "parms:" + str(self.params) + "\n"\
               + "verification:" + str(self.verifications) + "\n"
class MetaCases(metaclass= ABCMeta):

    def __init__(self, casefile):
        self.metaCases = None
        logger.log_info("Load metacase: " + casefile)
        self.content = load_file(casefile)
        if self.content is None:
            raise exceptions.MetaCaseFormatFailure("metacase file is empty")
        else:
            self.metaCases = self.content["metatcases"]
        logger.log_info(str(self.content))



    def __del__(self):
        """
        destructor function using for generate testing file at end.
        :return:
        """
        pass


    def getCases(self):
        request = APIRequest(self.content)
        self.metaCases = self._getMetaCases(request)
        return self.metaCases

    def _getMetaCases(self,request: APIRequest):
        #todo if not define
        cases = list()
        if self.metaCases is None or len(self.metaCases) == 0:
            cases.append(MetaCase(request,None))
            return cases
        logger.log_info("Loading metacase : " + str(len(self.metaCases)))
        for metacase in self.metaCases:
            cases.append(MetaCase(request,metacase))
        return cases

    def __repr__(self):
        if self.metaCases is not None:
            for caseInfo in self.metaCases:
                return "metacase info-> "+ str(caseInfo)
        else:
            return "object is None"




