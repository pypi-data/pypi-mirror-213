import heapq
import os


class Storage:
    def __init__(self):
        """
        :param filename: 文件名称
        :param path: 路径，当为空时为当前目录
        """
        self.filename = ""
        self.path = ""
        self.data = []

    def push(self, item):
        """
        写入
        :param data: dict 结构内必须包含id键用于排序
        """
        heapq.heappush(self.data, (item['id'], item))

    def pop(self):
        """
        以升序获取第一个元素并删除
        :return:
        """
        return heapq.heappop(self.data)

    def has_item(self):
        """
        判断堆是否为空
        :return:bool
        """
        return bool(self.data)

    def save_all(self):
        """
        保存文件
        :return:
        """
        with open(self.filename, "a+") as f:
            while self.data:
                _, data = heapq.heappop(self.data)
                f.write(data["body"])
