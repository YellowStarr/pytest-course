# -*- coding: utf-8 -*-
# ---
# @File: myDriver
# @Author: QiuWenJing
# @Time: 二月 28, 2024
# @Description: google webdriver 驱动二次封装
# ---

from selenium import webdriver
from selenium.webdriver.common.by import By
from myutils.myLog import MyLog
from selenium.common import exceptions
import sys

class MyDriver:
    def __init__(self):
        MyLog.info("初始化浏览器驱动")
        options = webdriver.ChromeOptions()
        # 全屏 start-fullscreen
        # options.add_argument()
        options.add_experimental_option("detach", True) # 保持浏览器打开状态
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
        except Exception as e:
            MyLog.error("初始化浏览器驱动失败，检查驱动和浏览器版本。错误原因：" + e)

    def _find_By(self, by):
        if by == "id":
            method = By.ID
        elif by == 'class':
            method = By.CLASS_NAME
        elif by == "tag":
            method = By.TAG_NAME
        elif by == "xpath":
            method = By.XPATH
        elif by == "css":
            method = By.CSS_SELECTOR
        elif by == "link":
            method = By.LINK_TEXT
        elif by == "partlink":
            method = By.PARTIAL_LINK_TEXT
        else:
            method = None
        return method

    def get_driver(self):
        return self.driver

    def open_Chrome(self, url):
        MyLog.info("打开浏览器,跳转地址:%s"%url)
        self.driver.get(url)

    def close_Chrome(self):
        MyLog.info("=======关闭浏览器========")
        self.driver.quit()

    def find_Element(self, by, value):
        method = self._find_By(by)
        MyLog.info("查找页面元素{by}={value}".format(by=method,value=value))
        if method is None:
            MyLog.error("传入的查找方法错误: {by}".format(by=method))
            self.close_Chrome()
            sys.exit()
        try:
            element = self.driver.find_element(by=method, value=value)
            return element
        except exceptions.NoSuchElementException:
            MyLog.warning("未找到指定元素by: {by}, value: {value}".format(by=method, value=value))
            self.close_Chrome()
            sys.exit()

    def find_Elements(self, by, value):
        method = self._find_By(by)
        MyLog.info("查找页面元素{by}={value}".format(by=method,value=value))
        if method is None:
            MyLog.error("传入的查找方法错误: {by}".format(by=method))
            self.close_Chrome()
            sys.exit()
        try:
            elements = self.driver.find_elements(by=method, value=value)
            return elements
        except exceptions.NoSuchElementException:
            MyLog.warning("未找到指定元素by: {by}, value: {value}".format(by=method, value=value))
            self.close_Chrome()
            sys.exit()

    def find_sub_Elements(self, parent, by, value,):
        method = self._find_By(by)
        MyLog.info("查找页面元素{by}={value}".format(by=method,value=value))
        if method is None:
            MyLog.error("传入的查找方法错误: {by}".format(by=method))
            self.close_Chrome()
            sys.exit()
        try:
            elements =parent.find_elements(by=method, value=value)
            return elements
        except exceptions.NoSuchElementException:
            MyLog.warning("未找到指定元素by: {by}, value: {value}".format(by=method, value=value))
            self.close_Chrome()
            sys.exit()

    def find_sub_Element(self, parent, by, value,):
        method = self._find_By(by)
        MyLog.info("查找页面元素{by}={value}".format(by=method,value=value))
        if method is None:
            MyLog.error("传入的查找方法错误: {by}".format(by=method))
            self.close_Chrome()
            sys.exit()
        try:
            element =parent.find_element(by=method, value=value)
            return element
        except exceptions.NoSuchElementException:
            MyLog.warning("未找到指定元素by: {by}, value: {value}".format(by=method, value=value))
            self.close_Chrome()
            sys.exit()

    def action(self, el, act, value=None):
        """

        :param el:
        :param act: ['input','click']
        :param value: 输入框输入数据
        :return:
        """
        if act == 'input':
            el.send_keys(value)
        elif act == 'click':
            el.click()

    def _get_all_handlers(self):
        MyLog.info("========获取窗口所有句柄========")
        windows = self.driver.window_handles
        return windows

    def get_current_handler(self):
        return self.driver.current_window_handle

    def switch_handler(self, cur=-1):
        """切换窗口"""
        windows = self._get_all_handlers()
        self.driver.switch_to.window(windows[cur])

    def get_attr(self, el, attribut):
        MyLog.info("在元素{el}上查找属性{attr}".format(el=el,attr=attribut))
        try:
            if attribut == 'text':
                content = el.text
            else:
                content = el.get_attribute(attribut)
            return content
        except exceptions.NoSuchAttributeException:
            MyLog.warning("元素{el}上没有{attribute}属性".format(el=el, attribut=attribut))
            print("没有该属性")
