# -*- coding: utf-8 -*-
# ---
# @File: eastFactory
# @Author: QiuWenJing
# @Time: 二月 29, 2024
# @Description: 存放东方财富的主要页面元素
# ---

from webFactory.myDriver import MyDriver
import allure

class EastFactory(MyDriver):
    def __init__(self):
        super(EastFactory, self).__init__()

    @allure.description("顶部导航菜单")
    def nav_warehouse(self, ):
        """顶部导航菜单区域"""
        navlist = self.find_Element('class', 'navlist')
        elements = self.find_sub_Elements(navlist, 'tag', 'a')
        return elements

    @allure.description("搜索框")
    def search_warehouse(self):
        search_input = self.find_Element('id', 'code_suggest')
        # self.driver.action(search_input, 'input', "000001")
        search_btn = self.find_Element('id', "search_view_btn1")
        return {"search_input":search_input, "search_btn":search_btn}
