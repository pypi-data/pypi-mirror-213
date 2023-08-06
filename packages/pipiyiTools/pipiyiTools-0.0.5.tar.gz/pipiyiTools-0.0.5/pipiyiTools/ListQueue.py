#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：内容队列
@File    ：ListQueue.py
@Author  ：Pipiyi
@Date    ：24 /5/23 21:35 
"""


class ListQueue:
    def __init__(self):
        self.data = {}

    def get_all(self, key):
        return self.data.get(key, [])

    def set_items(self, key, value):
        """写入内容,如果有指定key则覆盖，没有则写入

        Args:
            key (_type_): _description_
            value (_type_): _description_
        """
        self.data["key"] = value

    def put(self, key, item):
        """
        压入内容
        :param key:
        :param item:
        :return:
        """
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(item)

    def pop(self, key):
        """
        返回最后一个元素并从队列删除该元素
        :return:
        """
        try:
            return self.data.get(key, []).pop()
        except IndexError:
            return None

    def has_items(self, key):
        """
        判断队列是否为空
        :return:
        """
        return len(self.data.get(key, [])) > 0

    def first(self, key):
        """
        返回队列第一个元素并删除
        :return:
        """
        try:
            return self.data.get(key, []).pop(0)
        except IndexError:
            return None
