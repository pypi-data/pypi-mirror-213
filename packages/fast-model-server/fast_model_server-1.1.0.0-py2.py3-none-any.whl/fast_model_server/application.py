# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务入口

Authors: fubo
Date: 2022/03/04 00:00:00
"""
import os
import sys
import inspect
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from importlib import import_module


class Application(object):
    def __init__(self, server_path: str, ui_path: str = "", log_file: str = "", backup_count=0):
        self.server_path = server_path
        Application.set_log(log_file, backup_count)
        self.app = FastAPI()
        self.register()
        if type(ui_path) is str and ui_path != "" and "/" in ui_path and ui_path.index("/") == 0:
            self.add_ui()
        self.add_dynamic_web()

    @staticmethod
    def set_log(log_file: str = "", backup_count=0):
        """
        设置日志
        :param log_file: 日志文件名
        :param backup_count: 日志保留数
        :return: 队列中无数据情况下，返回空字符串
        """
        log_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"

        if log_file == "":
            logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stderr)
        else:
            log_file_handler = TimedRotatingFileHandler(filename=log_file, when="D", interval=1,
                                                        backupCount=backup_count)
            log_file_handler.setFormatter(logging.Formatter(log_format))
            logging.basicConfig(level=logging.INFO, handlers=[log_file_handler])

    def register(self):
        """
        查找routers下面所有的router包，注册router
        :return:
        """
        routers_path = "%s/routers" % self.server_path
        packages = filter(
            lambda x: (
                    (not x.startswith("__")) and (not x.endswith("__")) and os.path.isdir("%s/%s" % (routers_path, x))
            ), [package_name for package_name in os.listdir(routers_path)]
        )
        for package_name in packages:
            import_module("routers.%s.router" % package_name)
            for name, cls in inspect.getmembers(sys.modules["routers.%s.router" % package_name]):
                if inspect.isclass(cls) and name == "Router":
                    router = cls()
                    self.app.include_router(router.router, prefix="")
                    # self.app.include_router(router.router, prefix="/%s" % router.name)

    def add_ui(self, ui_path: str = "/"):
        """
        添加前端页面
        :param ui_path: 前端UI映射的页面路径
        """
        # 注册跨域
        self.app.add_middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
        )

        # 挂载前端页面
        self.app.mount(ui_path, StaticFiles(directory="static"), name="static")

    def add_dynamic_web(self):
        """
        添加web页基础库
        """
        if not os.path.exists(self.server_path + "/web"):
            return

        web_path = "%s/web" % self.server_path
        packages = filter(
            lambda x: (
                    (not x.startswith("__")) and (not x.endswith("__")) and (not os.path.isdir("%s/%s" % (web_path, x)))
            ), [package_name for package_name in os.listdir(web_path)]
        )
        for package_file_name in packages:
            package_name = ".".join(package_file_name.split(".")[:-1])
            import_module("web.%s" % package_name)
            for name, cls in inspect.getmembers(sys.modules["web.%s" % package_name]):
                if inspect.isclass(cls) and name == "Web":
                    self.app.mount("/%s" % package_name, WSGIMiddleware(cls.application.server))
