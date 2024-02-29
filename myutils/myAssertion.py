# -*- coding: utf-8 -*-
# ---
# @File: myAssertion
# @Author: QiuWenJing
# @Time: 二月 02, 2024
# @Description: 验证类的封装
# ---

class MyAssertion:

    def equal(self, arg1, arg2):
        if type(arg1) == type(arg2):
            return arg1 == arg2
        else:
            return False

    def unequal(self, arg1, arg2):
        if type(arg1) == type(arg2):
            return not (arg1 == arg2)
        else:
            return False

            # 查找单个键

    def find(self,target, dictData):
        if isinstance(dictData, dict):
            queue = [dictData]
            while len(queue) > 0:
                data = queue.pop()
                for key, value in data.items():
                    if key == target:
                        return value

                    elif type(value) == dict: queue.append(value)
                    elif type(value) == list:
                        for i in range(len(value)):
                            self.find(target, value[i])
        else:
            raise TypeError(dictData+"不是字典类型")
        return False

    def contain(self,arg1, arg2):
        """
        包含关系判定。要求响应体是字典类型
        :param arg1: 响应体中的数据
        :param arg2: 期望数据
        :return:
        """
        # 响应体解包
        if isinstance(arg1, dict):
            print(arg2)
            for k, v in arg2.items():
                if k.find('$')>=0:
                    s = k.split('$')[1:][0]
                    print(s)
                    # data.0.rank
                    depth_l = s.split('.')
                    i = 0
                    data = arg1
                    while i < len(depth_l):
                        if isinstance(data, list):
                            depth_l[i] = int(depth_l[i])
                        if i == len(depth_l)-1:
                            target = data[depth_l[i]]
                            print(target == v)
                            return target == v
                        data = data[depth_l[i]]
                        i += 1
                else:
                    value = self.find(k, arg1)
                    if value:
                        return value == v
            return False

    def exclude(self, arg1, arg2):
        """
        不包含关系
        :param arg1:
        :param arg2:
        :return:
        """
        if isinstance(arg1, dict):

            if self.contain(arg1, arg2):
                return False
            else:
                return True




