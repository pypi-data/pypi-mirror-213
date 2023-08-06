# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-11:39
# @Author  : 灯下客
# @Email   : 
# @File    : file_loader.py
# @Software: PyCharm
import os

files_cached = {}


class FileLoader(object):
    default_file = None
    file_env_location = None
    path = None

    def __init__(self, path, default_filename):
        self.path = path
        self.default_file = default_filename

    def get_file(self, path=None, fn=None):
        if path is None:
            path = self.path
        if os.path.isdir(path):
            path = os.path.join(path, self.default_file)
        return self._get_conf_from_file(path, fn)

    def put_file(self, path, content, mode="w"):
        file_to_write = open(path, mode)
        file_to_write.write(content)  # The key is type bytes still
        file_to_write.close()

    def _get_conf_from_file(self, path, fn=None):
        if path and os.path.isdir(path):
            path = os.path.join(path, self.default_file)

        if not path or not os.path.isfile(path):
            return {}
        if path not in files_cached:
            self.path = path
            if fn:
                files_cached[path] = fn(path)
            else:
                file_to_read = open(path, "rb")
                content = file_to_read.read()  # The key will be type bytes
                file_to_read.close()
                files_cached[path] = content
        return files_cached[path]
