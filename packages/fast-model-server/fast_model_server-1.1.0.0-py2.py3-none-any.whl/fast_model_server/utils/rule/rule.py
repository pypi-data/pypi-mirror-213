# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【代码文件说明】

Authors: fubo
Date: 2022/10/3 10:06:00
"""
import copy
import logging
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
from rule_engine import Rule


class RuleConditionType(Enum):
    """
    规则条件类型
    """
    # 静态常量
    CONST_VALUE = 0

    # 预定义表达式
    PRE_DEFINE = 1

    # 自定义函数
    USER_DEFINE_FUNCTION = 2


class RuleCondition(BaseModel):
    """
    规则条件
    """
    # 条件类型
    type: RuleConditionType = RuleConditionType.CONST_VALUE

    # 条件内容
    value: Any = ""


class RuleAction(BaseModel):
    """
    规则操作函数
    """
    # 操作函数
    func: str = ""


class RuleTuple(BaseModel):
    """
    规则二元组
    """
    # 条件
    condition: RuleCondition = RuleCondition()

    # 操作函数
    action: RuleAction = RuleAction()


class RuleGroup(BaseModel):
    """
    规则组
    """
    # 规则组名称
    group_name: str = ""

    # 规则组内容
    rules_group: List[RuleTuple] = []


class RuleSet(BaseModel):
    # 规则集合名称
    set_name: str = ""

    # 规则集合
    rule_groups: List[RuleGroup] = []


class RuleBulk(BaseModel):
    # 规则组
    rule_group: RuleGroup = RuleGroup()

    # 条件数据
    condition_input: Dict = {}

    # 执行数据
    data_input: Dict = {}


class RuleEngine(object):
    def __init__(self, executor_count: int = 1):
        self.pool = ThreadPoolExecutor(max_workers=executor_count)

    def __del__(self):
        self.pool.shutdown()
        del self.pool

    def __check_condition(self, rule: RuleTuple, condition_input: Dict) -> bool:
        """
        条件检查
        :param rule 规则
        :param condition_input 条件数据
        """
        if rule.condition.type == RuleConditionType.CONST_VALUE:
            # 固定值
            if type(rule.condition.value) != bool:
                raise ValueError("Error condition value %s" % rule.condition.value)

            return rule.condition.value

        if rule.condition.type == RuleConditionType.PRE_DEFINE:
            # 预定义的规则
            return Rule(rule.condition.value).matches(condition_input)

        if rule.condition.type == RuleConditionType.USER_DEFINE_FUNCTION:
            # 自定义条件函数
            try:
                return getattr(self, rule.condition.value)(condition_input)
            except AttributeError as exp:
                logging.error("No such condition function named %s. [%s]", rule.condition.value, exp)
                raise ValueError("No such condition function named %s. [%s]" % (rule.condition.value, exp))

        return False

    def __run_action(self, rule: RuleTuple, data_input: Dict) -> bool:
        """
        执行action操作
        :param rule 规则
        :param data_input 用于计算数据
        """
        try:
            return getattr(self, rule.action.func)(data_input)
        except AttributeError as exp:
            logging.error("No such condition function named %s. [%s]", rule.condition.value, exp)
            raise ValueError("No such condition function named %s. [%s]" % (rule.condition.value, exp))

    def run_rule_group(self, rule_group_data: RuleBulk) -> Dict:
        """
        执行规则group
        :param rule_group_data
        """
        data = copy.deepcopy(rule_group_data.data_input)
        logging.info("Run rule group named %s", rule_group_data.rule_group.group_name)
        for rule in rule_group_data.rule_group.rules_group:
            if not self.__check_condition(rule=rule, condition_input=rule_group_data.condition_input):
                break
            data = self.__run_action(rule=rule, data_input=data)
        return data

    def run(self, bulk_data: List[RuleBulk]) -> List[Dict]:
        """
        执行规则
        """
        return list(self.pool.map(self.run_rule_group, bulk_data))
