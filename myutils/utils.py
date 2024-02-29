# -*- coding: utf-8 -*-
import os

class Utils:
    @staticmethod
    def origin(origin=None):
        if not origin:
            origin = "https://jsonplaceholder.typicode.com"
        else:
            origin = origin
        return origin


    @staticmethod
    def headers(headers=None):
        if not headers:
            headers = {
                               'Content-type': 'application/json; charset=UTF-8',
                           }
        else:
            headers = headers

        return headers

    def  switch_dir(self):
        print(dir(os))

