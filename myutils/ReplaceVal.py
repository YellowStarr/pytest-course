# -*- coding: utf-8 -*-
# ---
# @File: ReplaceVal
# @Author: QiuWenJing
# @Time: 一月 29, 2024
# @Description: yaml变量替换
# ---
import json
from myutils.yamlutil import YamlUtil
import os

def replace_val(data, args):
    """
    替换变量 变量格式需是${}
    :param data: 带${}的数据
    :param args: ${}中变量值的来源
    :return: 返回替换完成的数据
    """
    if data:
        data_type = type(data) # 保存数据原始类型
        print("data type:", data_type)

        if isinstance(data, dict) or isinstance(data, list):
            str_data = json.dumps(data)
            print(str_data)
        else:
            str_data = str(data)

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

        # 替换变量
        for x in range(len(arg)):
            val = get_value(arg[x],args)
            # if isinstance(val, dict) or isinstance(val, list):
            #     val = json.dumps(val)
            # else:
            #     val = str(val)
            #
            # str_data = str_data.replace(arg[x], val)

        # print("str_data",type(str_data))
        # 还原数据类型
        # if data_type == dict:
        #     json_string = str_data.replace("'", '"')  # 将单引号替换为双引号
        #     print(json_string)
        #     dictionary = json.loads(json_string)
        #     print(dictionary)





def get_value(k, d):
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



if __name__ == "__main__":
    # s = {"s1":"${a}sfs", "s2": "${444}"}
    # s = []


    d = {"b":1, 'a':3, '444': {"a1":2}}
    # key = replace_val(s,d)
    # print(get_value(key, d))

    # pattern = r"\${([^}]+)\}"
    # matches = re.findall(pattern, s)
    # print(matches)
    ym = YamlUtil().read_casedata_yaml()
    print(ym)
    # print(ym[2]["request"]["param"])

