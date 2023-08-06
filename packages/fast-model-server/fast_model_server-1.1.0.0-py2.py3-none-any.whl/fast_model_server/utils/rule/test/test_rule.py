# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则引擎测试

Authors: fubo
Date: 2022/12/28 21:15:00
"""
import os
import sys
import logging
from typing import List, Dict
from fast_model_server.utils.rule.rule import RuleEngine, RuleBulk, RuleSet


class TestRuleEngine(RuleEngine):
    def __init__(self, executor_count: int):
        super().__init__(executor_count)

    def condition_func(self, condition_input: Dict) -> bool:
        return "银行" in condition_input["ent_name"]

    def action_func(self, data_input: Dict) -> Dict:
        data_input["count"] = data_input["count"] + 1
        return data_input


def main():
    rule_engine = TestRuleEngine(executor_count=2)
    local_path = os.path.dirname(os.path.abspath(__file__))

    rules = RuleSet.parse_file(local_path + "/rules_test.json")
    c_data_a = {"ent_name": "百度在线网络技术北京有限公司"}
    c_data_b = {"ent_name": "中国农业银行股份有限公司"}

    bulk_data: List[RuleBulk] = [
        RuleBulk(rule_group=rules.rule_groups[0], condition_input=c_data_a, data_input={"count": 0}),
        RuleBulk(rule_group=rules.rule_groups[1], condition_input=c_data_b, data_input={"count": 0})
    ]
    print(rule_engine.run(bulk_data=bulk_data))


if __name__ == '__main__':
    log_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stderr)
    main()
