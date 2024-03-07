# -*- coding: utf-8 -*-

import os,sys
import yaml
import json
import pandas as pd
from myutils.myLog import MyLog
from configparser import ConfigParser

class YamlUtil:
    def __init__(self):

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.conf = ConfigParser()
        path = "pytest.ini"
        self.conf.read(path)

        # print(self.BASE_DIR)
        # r = cf.read("pytest.ini")
        # print(r.sections())

    def read_data(self, param_value):
        """
        读取数据包中的数据
        :param param_value: 数据包文件名
        :return: Dataframe
        """
        with open(os.getcwd()+ "\\testcase"+param_value, mode='r', encoding='utf-8') as f:
            # param_list = yaml.load(stream=f, Loader=yaml.FullLoader)
            param_list = yaml.safe_load(f)
            try:
                self._check_ddt(param_list)
                df = pd.DataFrame.from_records(param_list[1:], columns=param_list[0])
                return df
            except Exception:
                MyLog.error("测试数据包数据不全， 测试用例名"+param_value)
                sys.exit()

    def _check_ddt(self, paramlist):
        """检查数据包中数据完整性"""
        for row in range(1,len(paramlist)):
            args_length = len(paramlist[0])
            temp_length = len(paramlist[row])
            if args_length != temp_length:
                raise Exception("请补全数据")

        return True

    def clear_yaml_temp(self):
        if not os.path.exists(os.getcwd()+ "\\temp.yml"):
            current_dir = os.getcwd()  # 获取当前工作目录
            # parent_dir = os.path.dirname(current_dir)  # 获取当前工作目录的上级目录
            # parent_dir +
            path =  "\\temp\\temp.yml"
        else:
            path = os.getcwd()+ "\\temp.yml"
        with open(path, mode='a', encoding='utf-8') as f:
            MyLog.info("清空中间变量")
            f.truncate(0)


    def write_temp_yaml(self,data):
        """
        写中间变量值
        :param data:
        :return:
        """
        if not os.path.exists(os.getcwd()+ "\\temp.yml"):
            # current_dir = os.getcwd()  # 获取当前工作目录
            # parent_dir = os.path.dirname(current_dir)  # 获取当前工作目录的上级目录
            path = "\\temp\\temp.yml"
        else:
            path = os.getcwd()+ "\\temp.yml"
        MyLog.info("中间变量地址 {p}, 存储中间变量: {d}".format(p=path, d=json.dumps(data)))
        with open(path, mode='a', encoding='utf-8') as f:
            yaml.dump(data=data, stream=f,allow_unicode=True)


    def read_temp_yaml(self):
        """
        读取中间变量
        """
        if not os.path.exists(os.getcwd()+ "\\temp.yml"):
            # current_dir = os.getcwd()  # 获取当前工作目录
            # parent_dir = os.path.dirname(current_dir)  # 获取当前工作目录的上级目录
            path =  "\\temp\\temp.yml"
        else:
            path = os.getcwd()+ "\\temp.yml"
        MyLog.info("=========读取中间变量, 读取地址{p}==========".format(p=path))
        with open(path, mode='r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
        MyLog.info("=========读取中间变量, {v}==========".format(v=value))
        return value

    def _find_ymls(self):
        """
         根据pytest.ini配置中的testpaths，寻找对应路径下的全部yaml
        :return:
        """
        yaml_path =  self.conf.get("pytest", "testpaths")
        yaml_files = []
        for root,dirs,files in os.walk(yaml_path):
            # 筛选yaml
            for file in range(len(files)):
                # path = os.path.join(root, dirs)
                if files[file].split(".")[1] == 'yml':
                    y_path = os.path.join(yaml_path, files[file])
                    yaml_files.append(y_path)
        return yaml_files

    def _find_yml(self, filename):
        """
        根据pytest.ini配置中的testpaths，寻找对应路径下的yaml
        :return: yaml文件
        """
        yaml_path =  self.conf.get("pytest", "testpaths")
        # yaml_files = []

        for root,dirs,files in os.walk(yaml_path):
            # 筛选yaml
            for file in range(len(files)):
                # path = os.path.join(root, dirs)
                if files[file].split(".")[1] == 'yml':
                    if files[file] == filename:
                        y_path = os.path.join(yaml_path, files[file])
                        return y_path
        return False



    def read_casedata_yaml(self, filename=None):
        """
        读取测试用例.
        :param filename:
        :return:
        """
        if filename:
            path = self._find_yml(filename)
            with open(path, mode='r', encoding='utf-8') as f:
                value = yaml.load(stream=f, Loader=yaml.FullLoader)
                case_list = []
                for case in range(len(value)):
                    feature = value[case]["feature"]
                    story = value[case]["story"]
                    header = value[case]["request"]["header"]
                    url = value[case]["request"]["origin"] + value[case]["request"]["url"]
                    method = value[case]["request"]["method"]
                    param = value[case]["request"]["param"]
                    expect = value[case]["validator"]
                    extract = value[case]["extract"]
                    case_list.append((url, header, method, param, expect, extract, feature, story))
                return case_list

    def check_args(self, value):
        """检查数据中是否有变量"""
        if value:
            data_type = type(value)
            if isinstance(value, dict) or isinstance(value, list):
                str_data = json.dumps(value)
                print(str_data)
            else:
                str_data = str(value)
            if str_data.count('${') == 0:
                return
            else:
                # 将待替换的变量找出，并存储下来
                search_vals = str_data.count('${')
                start_index, end_index = 0,0
                arg = []
                while(search_vals >0):
                    start_index = str_data.find('${', start_index)+1
                    end_index = str_data.find('}', end_index)+1
                    old_value = str_data[start_index-1:end_index]
                    arg.append(old_value)
                    # print("old_value", old_value)
                    search_vals -= 1
                print("需要替换的变量数组",arg)
                # 替换变量
                args = self.read_temp_yaml()
                for x in range(len(arg)):
                    val = self.get_value(arg[x],args)
                    if isinstance(val, dict) or isinstance(val, list):
                        val = json.dumps(val)
                    else:
                        val = str(val)
                    str_data = str_data.replace(arg[x], val)
                if data_type == dict:
                    str_data = json.loads(str_data)
                return str_data

    def get_value(self,k, d):
        """
        获取
        :param k:
        :param d:
        :return:
        """
        key = k[2:-1]
        print(key)
        if key in d:
            val = d[key]
            return val




