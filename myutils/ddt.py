# -*- coding: utf-8 -*-
# ---
# @File: ddt.py
# @Author: QiuWenJing
# @Time: 二月 01, 2024
# @Description: 数据驱动工具类
# ---

import json
from myutils.yamlutil import YamlUtil
import os
import yaml
from myutils.myLog import MyLog


# 读取测试用例
def read_testcase(yaml_name):

    yaml_file = YamlUtil()._find_yml(yaml_name)
    MyLog.info("读取测试用例地址: "+yaml_file)
    with open(yaml_file, mode='r', encoding='utf-8') as f:
        caseinfo = yaml.load(f, yaml.FullLoader)
        MyLog.info("读取测试用例内容" + json.dumps(caseinfo))
        if len(caseinfo)>=2:   #判断yaml用例文件中有几条用例，当用例大于等于2时，直接返回caseinfo
            case_list = format_data(caseinfo)
            return case_list
        else:                    #当等于1时，因为数据驱动后的caseinfo是字典列表我们就需要对caseinfo解包
            if "parametrize" in dict(*caseinfo).keys():
                new_caseinfo = ddt(*caseinfo)

                MyLog.info("测试用例解析后:"+ json.dumps(new_caseinfo))

                print(type(new_caseinfo))
                case_list = format_data(new_caseinfo)
                print("==========1============",case_list)
                return case_list
            else:
                MyLog.info("测试用例解析后:"+ json.dumps(caseinfo))
                print("======================", type(caseinfo))
                case_list = format_data(caseinfo)
                print("===========2===========",case_list)
                return case_list

def format_data(caselist):
    c_list = []
    for case in range(len(caselist)):
        feature = caselist[case]["feature"]
        story = caselist[case]["story"]
        header = caselist[case]["request"]["header"]
        url = caselist[case]["request"]["origin"] + caselist[case]["request"]["url"]
        method = caselist[case]["request"]["method"]
        param = caselist[case]["request"]["param"]
        expect = caselist[case]["validator"]
        extract = caselist[case]["extract"]
        c_list.append((url, header, method, param, expect, extract, feature, story))
    return c_list

def ddt(caseinfo):
    if "parametrize" in caseinfo.keys():
        new_caseinfo = []
        caseinfo_str = json.dumps(caseinfo)  # 测试用例str化
        for param_key, param_value in caseinfo["parametrize"].items(): #从数据包中获取对应的数据

            key_list = param_key.split("-")  # 将param_key转成列表
            MyLog.info("参数化用例地址："+ param_key)
            data_df = YamlUtil().read_data(param_value)  # 获取数据包中的数据dataframe

        # 替换变量
        for idx, row in data_df.iterrows():

            temp_caseinfo = caseinfo_str
            for name in range(len(key_list)):
                # row[key_list[name]]
                if isinstance(row[key_list[name]], int) or isinstance(row[key_list[name]], float):
                    temp_caseinfo = temp_caseinfo.replace('"$ddt{' + key_list[name] + '}"', str(row[key_list[name]]))
                else:
                    temp_caseinfo = temp_caseinfo.replace("$ddt{" + key_list[name] + "}",str(row[key_list[name]]))

            new_caseinfo.append(json.loads(temp_caseinfo))
        return new_caseinfo
    else:
        return caseinfo



if __name__ == "__main__":
    print(read_testcase("ddt_test.yml"))
