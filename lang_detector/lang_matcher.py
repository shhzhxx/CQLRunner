from lang_detector.java_rule import JavaRuleChain
from utils import config


class LangMatcher(object):
    def __init__(self):
        self.lang_type = None
        self.__next_lang = None
        self.__next_rule = None

    def set_next_lang_in_chain(self, next_lang):
        self.__next_lang = next_lang

    def set_next_rule_in_chain(self, next_rule):
        self.__next_rule = next_rule

    def is_match(self, dir_to_check, task_list):
        if self.__next_rule is not None:
            rst = self.__next_rule.is_match(dir_to_check, task_list)
            if rst is True:
                config.detected_lang_set.add(self.__next_rule.lang_type)
        if self.__next_lang is not None:
            self.__next_lang.is_match(dir_to_check, task_list)

    @staticmethod
    def build_chain():
        instance = JavaRuleChain()
        return instance
