# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-11:40
# @Author  : 灯下客
# @Email   : 
# @File    : config.py
# @Software: PyCharm
import os.path

import anyconfig

from easy_config import Dict
from easy_config import FileLoader


class EasyConfig(object):

    def __init__(self, data=None, path=None, default_filename='config.yml'):
        self._d_ = Dict(data)
        if os.path.isfile(path):
            path = os.path.dirname(path)
        if path is None:
            path = os.path.dirname(__file__)
        self.path = path
        self._loader = FileLoader(path, default_filename)

    def __getattr__(self, item):
        return self._d_.get(item)

    @property
    def data(self):
        return self._d_

    def to_dict(self):
        return self._d_.to_dict()

    def update(self, *args, **kwargs):
        self._d_.update(*args, **kwargs)

    def load_file(self, path=None):
        config = self._loader.get_file(path, anyconfig.load)
        self._d_.update(config)

    def load_by_content(self, content, ac_parser='yml'):
        extension = ac_parser.lower() if ac_parser.lower() != "yml" else "yaml"
        support_ext = anyconfig.list_types()
        if extension not in support_ext:
            raise Exception(f"Unsupported file format, currently only supported: {','.join(support_ext)}")
        config_dict = anyconfig.loads(content, ac_parser=extension)
        self._d_.update(config_dict)
