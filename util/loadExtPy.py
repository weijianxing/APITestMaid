#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
import glob, importlib, os, pathlib, sys

from util import logger
from util.exceptions import ExtPyScriptMethodNotFoundError

import importlib.util
def load_ext_python_files(filedir=""):
    # The directory containing your modules needs to be on the search path.
    MODULE_DIR = os.getcwd()  + filedir
    sys.path.append(MODULE_DIR)
    # Get the stem names (file name, without directory and '.py') of any
    # python files in your directory, load each module by name and run
    # the required function.
    logger.log_info("load ext module path is : " + MODULE_DIR)

    py_files = glob.glob(os.path.join(MODULE_DIR, '*.py'))
    for py_file in py_files:
        module_name = pathlib.Path(py_file).stem
        module = importlib.import_module(module_name)
        #module.mikaj_laktom()

        #module.mikaj_laktom()



class CloneExtMoudles():
    def __init__(self,moduledir):
        MODULE_DIR = os.getcwd() + moduledir
        sys.path.append(MODULE_DIR)
        #new = type(CloneExtMoudle.__name__)
        py_files = glob.glob(os.path.join(MODULE_DIR, '*.py'))
        for py_file in py_files:
            module_name = pathlib.Path(py_file).stem
            module = importlib.import_module(module_name)
            old = type(module.__name__)
            self.__dict__.update(old.__dict__)
        print("self dict is : " + str(self.__dict__))
class CloneExtMoudle():
    def __init__(self,modulefile,class_name="ExtPy", apiData = {}):
        """

        :param modulefile:
        :param class_name:
        """
        #todo judgement dir type.
        module_name = os.getcwd() + str(os.path.sep) + modulefile
        #module = importlib.import_module(module_name)
        #module = importlib.util.cache_from_source(module_name)
        spec = importlib.util.spec_from_file_location(class_name, module_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Optional; only necessary if you want to be able to import the module
        # by name later.
        sys.modules[module_name] = module
        self.ext_class = getattr(module, class_name)
        self.ext_instance = self.ext_class()
        self.data = apiData
    def exec_method(self,methodname,*args):
        """

        """
        logger.log_info("exec_method : method name is : " + methodname + " : params : " + str(args))
        # if len(args) == 0 or args[0] == "$response":
        #     del args
        #     args = (self.data,)
        temp = args
        del args
        args = (self.data,) + temp
        if hasattr(self.ext_class, methodname):
            method = getattr(self.ext_instance, methodname)
            return method(*args)
        else:
            raise ExtPyScriptMethodNotFoundError("user defined hook method : " + methodname + " not found.")

if __name__ == "__main__":

    pydir = ""
