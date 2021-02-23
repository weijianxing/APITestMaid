import yaml
import io
import json
from util import logger
from util import exceptions
import os
import fire
try:
    # PyYAML version >= 5.1
    # ref: https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
    yaml.warnings({'YAMLLoadWarning': False})
except AttributeError:
    pass
#global
conf = {}


def _load_yaml_file(yaml_file):
    """ load yaml file and check file content format
    """
    with io.open(yaml_file, 'r', encoding='utf-8') as stream:
        yaml_content = None
        try:
            yaml_content = yaml.load(stream)
        except yaml.YAMLError as ex:
            logger.log_error(str(ex))
            #raise

        return yaml_content


def _load_json_file(json_file):
    """ load json file and check file content format
    """
    with io.open(json_file, encoding='utf-8') as data_file:
        try:
            json_content = json.load(data_file)
        except json.JSONDecodeError:
            err_msg = u"JSONDecodeError: JSON file format error: {}".format(json_file)
            logger.log_error(err_msg)
            #raise exceptions.FileFormatError(err_msg)

        return json_content

def load_file(file_path):
    if not os.path.isfile(file_path):
        raise exceptions.FileNotFound("{} does not exist.".format(file_path))

    file_suffix = os.path.splitext(file_path)[1].lower()
    if file_suffix == '.json':
        return _load_json_file(file_path)
    elif file_suffix in ['.yaml', '.yml']:
        return _load_yaml_file(file_path)
    else:
        # '' or other suffix
        err_msg = u"Unsupported file format: {}".format(file_path)
        logger.log_warning(err_msg)

        return []
def testload(filename="crowed.yml"):
    """docstring for testload"""
    global conf
    conf = load_file(filename)
    logger.log_info(json.dumps(conf,indent=4, sort_keys=True))
    logger.log_info(str(conf["sendMsgWhenFail"]))
    logger.log_info(str(conf["dingToken"]))
    logger.log_info(str(conf["caseTitle"]))
    logger.log_info(str(conf["atowners"]))
    logger.log_info('-----end------')
    #json prety format.
def loadMonitorConf(filename = "crowed.yml"):
    """docstring for load"""
    conf = load_file(filename)
    return conf


def sendfailinkes(page, links):
    """docstring for sendfailinkes
       :page It is the page monitored
       :links the brokened links in the page have been found
    """

class DingConfig():
    def __init__(self):
        self.token = ""
        self.atUser = []

def load_folder_files(folder_path, recursive=True):
    """ load folder path, return all files endswith yml/yaml/json in list.

    Args:
        folder_path (str): specified folder path to load
        recursive (bool): load files recursively if True

    Returns:
        list: files endswith yml/yaml/json
    """
    if isinstance(folder_path, (list, set)):
        files = []
        for path in set(folder_path):
            files.extend(load_folder_files(path, recursive))

        return files

    if not os.path.exists(folder_path):
        return []

    file_list = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        filenames_list = []

        for filename in filenames:
            if not filename.endswith(('.yml', '.yaml', '.json')):
                continue

            filenames_list.append(filename)

        for filename in filenames_list:
            file_path = os.path.join(dirpath, filename)
            file_list.append(file_path)

        if not recursive:
            break

    return file_list
if __name__ == '__main__':
    #filename = 'crowed.yml'
    #conf = load_file(filename)
    #json prety format.
    #logger.log_info(json.dumps(conf,indent=4, sort_keys=True))
    loadMonitorConf()

    fire.Fire(testload)


