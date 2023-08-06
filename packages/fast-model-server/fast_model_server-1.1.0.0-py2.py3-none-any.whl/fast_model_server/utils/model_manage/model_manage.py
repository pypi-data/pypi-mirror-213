# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型管理代码

Authors: fubo
Date: 2022/03/14 00:00:00
"""
import logging
import os
import sys
import tempfile
import argparse
from pydantic import BaseModel
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient


class BosInfo(BaseModel):
    # BOS ak
    ak: str

    # BOS sk
    sk: str

    # BOS end_point
    end_point: str

    # 本地模型仓库
    model_hub: str


class ModelManage(object):
    def __init__(self):
        self.local_path = os.path.dirname(os.path.abspath(__file__))
        self.pack_shell = "%s/pack.sh" % self.local_path
        self.config = BosInfo.parse_file(self.local_path + "/model_manage.config.json")
        self.config.model_hub = os.path.expanduser(self.config.model_hub)
        self.bos_client = BosClient(
            BceClientConfiguration(
                credentials=BceCredentials(self.config.ak, self.config.sk),
                endpoint = self.config.end_point
            )
        )

    def download(self, model_name: str, model_tag: str) -> str:
        """
        下载模型
        :param model_name: 模型文件名
        :param model_tag: 模型tag
        :return: 操作正常返回模型路径
        """
        if not os.path.exists(self.config.model_hub):
            os.system("mkdir %s" % self.config.model_hub)

        with tempfile.TemporaryDirectory() as work_path:
            download_file = "%s/%s" % (work_path, model_tag)
            self.bos_client.get_object_to_file("acg-fsu-alg-models", "%s/%s" % (model_name, model_tag), download_file)
            os.system("cd %s; tar -xzf %s" % (work_path, download_file))
            os.system("rm -rf %s" % download_file)
            name = os.listdir(work_path)[0]
            output_path = "%s/%s" % (self.config.model_hub, name)
            if os.path.exists(output_path):
                os.system("rm -rf %s" % output_path)
            os.system("mv %s/%s %s" % (work_path, name, output_path))
            os.system("rm -rf %s" % download_file)
        return output_path

    def upload(self, model_name: str, src_model_path: str) -> str:
        """
        上传模型，返回模型tag
        :param
        """
        # 上传模型的文件夹全路径
        src_model_path = src_model_path.strip("/")

        # 上传模型的文件夹
        model_path_last_level = src_model_path.split("/")[-1]

        # 上传模型部分路径
        model_path_rev_level = "/" + "/".join(src_model_path.split("/")[:-1])

        # 上传的文件
        upload_file = ""
        with tempfile.TemporaryDirectory() as work_path:
            os.system("bash %s %s %s %s" % (self.pack_shell, model_path_last_level, model_path_rev_level, work_path))
            for name in os.listdir(work_path):
                if "model_file_XXX_" in name and name.index("model_file_XXX_") == 0:
                    upload_file = name
                    break

            if upload_file == "":
                return ""
            self.bos_client.put_object_from_file(
                "acg-fsu-alg-models", "%s/%s" % (model_name, upload_file), work_path + "/" + upload_file
            )
        return upload_file


def main():
    """
    模型管理工具
    """
    log_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", type=str, help="Operation[download|upload]")
    parser.add_argument("model_name", type=str, help="Model Name")
    parser.add_argument("--model_tag", type=str, default="", help="Model Tag")
    parser.add_argument("--src_model_path", type=str, default="", help="Source Model Path")
    args = parser.parse_args()
    model_manage = ModelManage()
    operation = args.operation.lower()
    if operation not in ["download", "upload"]:
        logging.error("Error operation code %s", args.operation)
        return -1

    if operation == "download" and args.model_tag == "":
        logging.error("Empty model tag")
        return -2

    if operation == "upload" and args.src_model_path == "":
        logging.error("Empty src_model_path")
        return -3

    if operation == "download":
        print(model_manage.download(model_name=args.model_name, model_tag=args.model_tag))
        return 0

    if operation == "upload":
        print(model_manage.upload(model_name=args.model_name, src_model_path=args.src_model_path))
        return 0

    return 0


if __name__ == '__main__':
    main()
