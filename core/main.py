#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import json
import os
import sys
import traceback
from abc import ABCMeta

import fire
from com.wuage.testing.helper.chatbotHelper import DingtalkChatbot

from core.MetaCases import MetaCases, APIRequest
from util import logger
from util.generatorReport.Generator import Generator
from util.loadConfig import load_folder_files, load_file


def log_assertFail():
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)  # Fixed format
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]
    return 'Assert fail on line {} in statement {}'.format(line, text)
def print_exception():
    import linecache
    linecache.checkcache()
    efile = sys.stderr
    typ, val, tb = excinfo = sys.exc_info()
    sys.last_type, sys.last_value, sys.last_traceback = excinfo
    tbe = traceback.extract_tb(tb)
    print(efile, '\nTraceback (most recent call last):')

    traceback.print_list(tbe, file=efile)
    lines = traceback.format_exception_only(typ, val)
    for line in lines:
        print(efile, line)

class Main(metaclass = ABCMeta):
    def __init__(self,caseDir="/",configFileName = "/"):
        """

        :param caseDir: execution cases dir
        :param configFileName: configuration file dir
        """
        if caseDir == "/":
            self.metacasedir = os.getcwd() + caseDir + "/metacase"
            self.testcasedir = os.getcwd() + caseDir + "/testcase"
            self.testscenariodir = os.getcwd() + caseDir + "testscenario"

        else:
            self.metacasedir = os.getcwd() + caseDir
            self.testcasedir = os.getcwd() + caseDir
            self.testscenariodir = os.getcwd() + caseDir
        if configFileName == "/":
            self.confdir = os.getcwd()+configFileName + "/config/alter.yaml"
        else:
            self.confdir = os.getcwd() + configFileName
        logger.log_info("load matacases from : " + self.metacasedir)
        logger.log_info("load testcases from : " + self.testcasedir)
        logger.log_info("load testscenarios from : " + self.testscenariodir)

        self._metacases = {}

        self.resultdatafileName = 'util/Data/reportData.json'
        self.exec_result = list()
        self.htmlReportfileName = ""


    def __del__(self):
        #todo filter execution result.
        with open(self.resultdatafileName, 'w', encoding='utf-8') as f:
            json.dump(self.exec_result, f, ensure_ascii=False, indent=4)
            f.close()
        pass


    def load_metaCases(self):
        self.filelist = load_folder_files(self.metacasedir)
        for casefile in self.filelist:
            logger.log_info("begin loading matacase: " + casefile)
            meta = MetaCases(casefile)
            cases = meta.getCases()
            logger.log_info("meta cases : " + str(meta))

            # dict key is file: value is matacases.
            self._metacases[casefile] = cases
    def execute_metacases(self):
        """
        check and filter run testcases then execute
        :return:
        """
        for filename , metacases in self._metacases.items():
            logger.log_info("begin execute metacases : " + filename)

            for metacase in metacases:
                result = {}
                dirs = str(filename).split(os.sep)
                result["Application"] = dirs[-1]
                result["Environment"] = ""
                result["Id"] = metacase.caseName
                result["Test-Case"] = metacase.caseName
                result["APIType"] = metacase.apiType
                result["Error"] = []

                try:
                    #todo deal with  type cases [skipped,]
                    metacase.execute_verify()
                    result["Result"] = "Passed"
                # except AssertionError:
                except Exception :
                    # _, _, tb = sys.exc_info()
                    # traceback.print_tb(tb)  # Fixed format
                    formatted_lines = traceback.format_exc().splitlines()
                    # print(str(formatted_lines))
                    # exc_type, exc_value, exc_traceback = sys.exc_info()
                    # print("format execption.")
                    # print(repr(traceback.format_exception(exc_type, exc_value,
                    #                                 exc_traceback)))
                    # tb_info = traceback.extract_tb(tb)
                    # filename, line, func, text = tb_info[-1]
                    msg = 'Assert fail : {0}'.format(str(formatted_lines))
                    logger.log_error("execute fail: " + msg)
                    result["Result"] = "Failed"
                    # msg = log_assertFail()
                    # logger.log_error("asert fail : "+ msg)
                    errorInfos = []
                    infos = {}
                    infos["Description"] = msg
                    infos["Assert"] = "xxx"
                    infos["Screenshot"] = {
                                        "Name": "Screenshot-1.png",
                                        "Url": "#"
                                      }
                    errorInfos.append(infos)
                    result["Error"] = errorInfos
                finally:
                    self.exec_result.append(result)


            #self._metacases.append(metacase)``
    def execute_testcases(self):
        pass

    def execute_testscenarios(self):
        pass

    def genarate_testReport(self):
        """
        产生测试报告
        :return:
        """
        a = Generator(appName="search_report",
                      templatePath="util/Templates/",
                      reportPath="",
                      dataPath=self.resultdatafileName)
        a.generate_html()
        pass
    def getFailInfo(self):
        """
        check report when find fail case return model name.
        :return:
        """
        for result in self.exec_result:
            if result["Result"] == "Failed":
                failmodel = result["Application"]
                error = str(result["Error"])
                return failmodel, error
        logger.log_info("execute success.")
        return None,None



    def send_failMsg(self,failLink):
        """
        检查执行结果并发送失败信息到钉钉群
        内部方法，CLI方式应该从文件读取数据
        :return:
        """
        failmodel, errorInfo = self.getFailInfo()
        print("send fail info: " + str(failmodel))
        print("send error info : " + str(errorInfo))
        if failmodel is not None:
            #loading sending detail.
            conf = load_file(self.confdir)

            alter = conf["sendMsgWhenFail"]
            if str(alter) == 'False':
                logger.init("user donot config send alter when script execute fail. ")
                return
            token = conf["dingToken"]
            ding = DingtalkChatbot(webhook=token)
            subTitle = "API model {0} execute fail:".format(failmodel)
            print(subTitle)
            at_mobiles = conf["atowners"]
            print(at_mobiles)
            ding.send_failInfo(title="API testing.",
                               subTitle=subTitle
                               , owner=conf["owner"]
                               , at_mobiles=at_mobiles
                               ,reporturl=failLink
                               ,caseInfo= errorInfo)
        else:
            logger.log_info("skip sending msg.")

def test_meta(caseDir = "/"):
    """
    执行所有独立cases : caseDir: case所存放的路径，默认当前路径，如果自定义路径 仅支持在当前目录下创建
    :param caseDir: case所存放的路径，默认当前路径，如果自定义路径 仅支持在当前目录下创建
    :return:
    """

    main = Main(caseDir)
    main.load_metaCases()
    main.execute_metacases()

def main2():
    fire.Fire()

# if __name__ == '__main__':
#
#     fire.Fire()


