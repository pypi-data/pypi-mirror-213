# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务操作代码

Authors: fubo01
Date: 2022/03/04 00:00:00
"""
import sys
import argparse
import json
import os
import logging
from typing import List
from datetime import datetime
from pydantic import BaseModel


class RouterInfo(BaseModel):
    # 创建路由的路径
    path: str = ""

    # 路由名称
    name: str = ""

    # 模型名称
    model_name: str = ""

    # 模型tag
    model_tag: str = ""


class ServerInfo(BaseModel):
    # 创建服务的路径
    path: str = ""

    # 服务名称
    name: str = ""

    # web路径
    web_name: str = ""

    # 服务host
    host: str = "0.0.0.0"

    # 服务端口
    port: int = 8000

    # 服务工作进程数量
    worker_num: int = 2


class RouterConfig(BaseModel):
    # 路由名称
    name: str = "路由名称"

    # 模型名称
    model_name: str = "模型名称"

    # 模型tag
    model_tag: str = "模型tag"


class AppConfig(BaseModel):
    # 开发者邮箱前缀
    email_prefix: str = "开发者邮箱前缀"

    # server名称
    server_name: str = "server名称"

    # server路径
    server_path: str = "server路径"

    # web名称
    web_name: str = ""

    # 服务host
    host: str = "0.0.0.0"

    # 服务端口
    port: int = 8000

    # 服务工作进程数量
    worker_num: int = 1

    routers: List[RouterConfig] = [RouterConfig()]


class Operate:
    def __init__(self):
        self.email_prefix = ""
        self.curr_path = os.path.dirname(os.path.abspath(__file__))

        # server templates
        self.server_template_path = "%s/template/server" % self.curr_path
        self.start_sever_shell_template = self.load_template("%s/start.sh.template" % self.server_template_path)
        self.stop_sever_shell_template = self.load_template("%s/stop.sh.template" % self.server_template_path)
        self.docker_file_template = self.load_template("%s/Dockerfile.template" % self.server_template_path)
        self.server_py_template = self.load_template("%s/server.py.template" % self.server_template_path)

        # router templates
        self.router_template_path = "%s/template/router" % self.curr_path
        self.router_py_template = self.load_template("%s/router.py.template" % self.router_template_path)
        self.common_py_template = self.load_template("%s/common.py.template" % self.router_template_path)
        self.service_py_template = self.load_template("%s/service.py.template" % self.router_template_path)

        # web templates
        self.web_template_path = "%s/template/web" % self.curr_path
        self.web_py_template = self.load_template("%s/web.template" % self.web_template_path)

    def load_template(self, template_file: str) -> str:
        """
        加载模板文件
        :param template_file:
        :return:
        """
        with open(template_file, "r") as fp:
            content = [line.strip("\r\n") for line in fp.readlines()]
        return "\n".join(content)

    def fill_server_py_template(self, template: str) -> str:
        """
        填充服务代码文件
        :param template:
        :param server_info:
        :return:
        """
        return template.replace(
            "[email_prefix]", self.email_prefix
        ).replace(
            "[date]", datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        )

    def fill_web_py_template(self, template: str) -> str:
        """
        填充web代码文件
        :param template:
        :return:
        """
        return template.replace(
            "[email_prefix]", self.email_prefix
        ).replace(
            "[date]", datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        )

    def fill_server_shell_template(self, template: str, server_info: ServerInfo, is_local=False) -> str:
        """
        填充服务脚本文件
        :param template:
        :param server_info:
        :param is_local: 是否生成本地执行脚本
        :return:
        """
        template = template.replace(
            "[host]", server_info.host).replace(
            "[port]", str(server_info.port)).replace(
            "[worker_num]", str(server_info.worker_num)
        )
        if is_local is True:
            template = template.replace("/root/miniconda3/bin/", "")

        return template

    def fill_server_docker_file_template(self, template: str, server_info: ServerInfo) -> str:
        """
        填充服务Dockerfile文件
        :param template:
        :param server_info:
        :return:
        """
        server_name_hbar = server_info.name.replace("_", "-")
        return template.replace(
            "[server_name]", server_info.name).replace(
            "[server_name_hbar]", server_name_hbar
        )

    def fill_router_py_template(self, template: str, router_info: RouterInfo) -> str:
        """
        填充路由代码文件
        :param template:
        :param server_info:
        :return:
        """
        return template.replace(
            "[email_prefix]", self.email_prefix
        ).replace(
            "[date]", datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ).replace(
            "[router_name]", router_info.name
        ).replace(
            "[camel_router_name]", self.snake2camel(router_info.name)
        )

    def write_file(self, code_value: str, code_file: str):
        """
        代码写入到文件中
        :param code_value:
        :param code_file:
        :return:
        """
        with open(code_file, "w") as fp:
            fp.write(code_value)

    def snake2camel(self, name: str):
        """
        蛇形字符串转驼峰
        :param name:
        :return:
        """
        return "".join([elem.capitalize() for elem in name.split("_")])

    def create_server_structure(self, server_operate_path: str):
        """
        创建服务代码结构
        :param server_operate_path:
        :return:
        """
        os.system("mkdir %s" % server_operate_path)
        os.system("mkdir %s/routers" % server_operate_path)
        os.system("mkdir %s/configs" % server_operate_path)
        os.system("mkdir %s/static" % server_operate_path)

    def create_router_structure(self, router_operate_path: str):
        """
        创建路由代码结构
        :param server_operate_path:
        :return:
        """
        os.system("mkdir %s" % router_operate_path)
        os.system("mkdir %s/configs" % router_operate_path)
        os.system("mkdir %s/resources" % router_operate_path)
        os.system("mkdir %s/test" % router_operate_path)

    def create_web_structure(self, server_operate_path: str, web_name: str):
        """
        创建网页代码结构
        :param server_operate_path:
        :param web_name:
        :return:
        """
        os.system("mkdir %s/web" % server_operate_path)
        self.write_file(code_value="", code_file="%s/web/__init__.py" % server_operate_path)
        self.write_file(
            code_value=self.fill_web_py_template(self.web_py_template),
            code_file="%s/web/%s.py" % (server_operate_path, web_name)
        )

    def add_router_model_mapping(self, router: RouterInfo):
        """
        为router添加模型映射
        """
        if router.model_name == "":
            return
        mapping_file = "%s/../configs/models.mapping" % router.path
        if not os.path.exists(mapping_file):
            os.system("touch %s" % mapping_file)

        with open(mapping_file, "w") as fp:
            fp.write("%s|%s|%s" % (router.name, router.model_name, router.model_tag))
        return

    def create_router(self, router_info: RouterInfo = None) -> bool:
        """
        收集信息创建router
        :return:
        """
        if not os.path.isdir(router_info.path):
            print("输入的路由路径为非路径[%s]" % router_info.path)
            return False

        if not router_info.name.islower():
            print("路由名称不符合规范，参考python编码规范中对python包名称的定义")
            return False

        router_info.model_name = router_info.model_name.strip("\r\n\t").strip(" ")
        router_info.model_tag = router_info.model_tag.strip("\r\n\t").strip(" ")

        if router_info.model_name != "" and router_info.model_tag == "":
            print("模型没有提供tag，重新确认模型是否存在")
            return False

        operate_path = "%s/%s" % (router_info.path, router_info.name)
        if os.path.exists(operate_path):
            print("目录已经存在")
            return False

        self.create_router_structure(operate_path)
        self.write_file(
            code_value="",
            code_file="%s/configs/config.json" % operate_path
        )
        self.write_file(
            code_value="",
            code_file="%s/resources/resources.placeholder" % operate_path
        )
        self.write_file(
            code_value="", code_file="%s/__init__.py" % operate_path
        )
        self.write_file(
            code_value="", code_file="%s/test/__init__.py" % operate_path
        )
        self.write_file(
            code_value=self.fill_router_py_template(self.router_py_template, router_info),
            code_file="%s/router.py" % operate_path
        )
        self.write_file(
            code_value=self.fill_router_py_template(self.service_py_template, router_info),
            code_file="%s/service.py" % operate_path
        )
        self.write_file(
            code_value=self.fill_router_py_template(self.common_py_template, router_info),
            code_file="%s/common.py" % operate_path
        )
        self.add_router_model_mapping(router=router_info)
        return True

    def create_server(self, server_info: ServerInfo, router_names: List[str]) -> bool:
        """
        收集信息创建server
        :return:
        """
        if not os.path.isdir(server_info.path):
            print("输入的服务路径为非路径")
            return False

        if not server_info.name.islower():
            print("服务名称不符合规范，参考python编码规范中对python包名称的定义")
            return False

        operate_path = "%s/%s" % (server_info.path, server_info.name)
        if os.path.exists(operate_path):
            print("目录已经存在")
            return False

        # 创建代码框架
        self.create_server_structure(server_operate_path=operate_path)

        # 创建web代码包
        if server_info.web_name != "":
            self.create_web_structure(server_operate_path=operate_path, web_name=server_info.web_name)

        self.write_file(code_value="", code_file="%s/__init__.py" % operate_path)
        self.write_file(code_value="", code_file="%s/routers/__init__.py" % operate_path)

        # 服务配置数据
        server_config_data = {
            "env": ""
        }
        for router_name in router_names:
            server_config_data[router_name] = {}

        # 开发环境
        server_config_data["env"] = "dev"
        self.write_file(
            code_value=json.dumps(server_config_data, ensure_ascii=False, indent=4),
            code_file="%s/configs/dev.config.json" % operate_path
        )

        # 测试环境
        server_config_data["env"] = "test"
        self.write_file(
            code_value=json.dumps(server_config_data, ensure_ascii=False, indent=4),
            code_file="%s/configs/test.config.json" % operate_path
        )

        # 线上环境
        server_config_data["env"] = "prod"
        self.write_file(
            code_value=json.dumps(server_config_data, ensure_ascii=False, indent=4),
            code_file="%s/configs/prod.config.json" % operate_path
        )

        self.write_file(
            code_value="<html><body>Demo Test</body></html>", code_file="%s/static/index.html" % operate_path
        )

        self.write_file(
            code_value=self.fill_server_py_template(self.server_py_template),
            code_file="%s/server.py" % operate_path
        )
        self.write_file(
            code_value=self.fill_server_shell_template(self.start_sever_shell_template, server_info),
            code_file="%s/start.sh" % operate_path
        )
        self.write_file(
            code_value=self.fill_server_shell_template(self.stop_sever_shell_template, server_info),
            code_file="%s/stop.sh" % operate_path
        )

        self.write_file(
            code_value=self.fill_server_shell_template(self.start_sever_shell_template, server_info, is_local=True),
            code_file="%s/start_local.sh" % operate_path
        )
        self.write_file(
            code_value=self.fill_server_shell_template(self.stop_sever_shell_template, server_info),
            code_file="%s/stop_local.sh" % operate_path
        )

        self.write_file(
            code_value=self.fill_server_docker_file_template(self.docker_file_template, server_info),
            code_file="%s/Dockerfile" % operate_path
        )
        os.system("touch %s/%s/configs/models.mapping" % (server_info.path, server_info.name))

        return True

    @staticmethod
    def create_server_config_file(config_file: str):
        """
        创建服务需要的配置
        """
        with open(config_file, "w") as fp:
            fp.write(json.dumps(AppConfig().dict(), ensure_ascii=False, indent=4, separators=(',',':')))

    def create_server_from_config(self, config_file: str):
        """
        用配置文件创建服务
        """
        config: AppConfig = AppConfig.parse_file(config_file)
        self.email_prefix = config.email_prefix
        server_info = ServerInfo()
        server_info.path = config.server_path
        server_info.name = config.server_name
        server_info.host = config.host
        server_info.port = config.port
        server_info.worker_num = config.worker_num
        server_info.web_name = config.web_name
        self.create_server(server_info=server_info, router_names=[elem.name for elem in config.routers])
        for router in config.routers:
            router_info: RouterInfo = RouterInfo()
            router_info.name = router.name
            router_info.model_name = router.model_name
            router_info.model_tag = router.model_tag
            router_info.path = "%s/%s/routers" % (server_info.path, server_info.name)
            self.create_router(router_info=router_info)


def main():
    """
    生成代码结构配置文件或者根据配置文件生成代码结构
    """
    log_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stderr)
    parser = argparse.ArgumentParser(description="Server Creator")
    parser.add_argument("config_file", type=str, help="application config file")
    parser.add_argument("--generate", default=False, action='store_true', help="Generate application config")
    args = parser.parse_args()
    op = Operate()
    config_file = args.config_file
    for_generate = args.generate
    if for_generate:
        op.create_server_config_file(config_file)
        return 0

    op.create_server_from_config(config_file)
    return 0


if __name__ == '__main__':
    main()
