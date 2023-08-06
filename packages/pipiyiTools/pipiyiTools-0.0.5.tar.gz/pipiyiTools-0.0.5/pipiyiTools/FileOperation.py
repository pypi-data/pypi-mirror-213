#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：文件读写
@File    ：FileOperation.py
@Author  ：Pipiyi
@Date    ：25/5/23 12:22 
"""

import os


class FileOperation:
    @staticmethod
    def put(filename, data):
        """
        追加写入文件
        :param filename: 文件名
        :param data: 内容
        :return:
        """
        with open(filename, "a+") as f:
            f.write(data)

    @staticmethod
    def read_file_to_list(filename):
        """
        读取文件并以每行作为分隔转为列表
        :param filename: 文件名
        :return:
        """
        try:
            with open(filename, "r") as f:
                content = f.readlines()
                return [line.strip() for line in content]
        except Exception:
            return None

    @staticmethod
    def remove(file):
        """
        删除指定文件
        :param file:
        :return:
        """
        try:
            os.remove(file)
        except Exception as e:
            raise Exception(e)
