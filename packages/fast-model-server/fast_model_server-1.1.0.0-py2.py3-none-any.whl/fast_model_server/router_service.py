# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RouterService抽象类

Authors: fubo01
Date: 2022/04/09 23:21:00
"""
from fast_model_server.common import ServerConfig


class RouterService(object):
    def __init__(self, server_config_file: str):
        config = ServerConfig.parse_file(server_config_file)
        self.env = config.env
