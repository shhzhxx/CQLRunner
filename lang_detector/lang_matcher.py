from lang_detector.java_rule import JavaRuleChain


class LangMatcher(object):
    def __init__(self):
        self.lang_type = None
        self.__next_lang = None
        self.__next_rule = None

    def set_next_lang_in_chain(self, next_lang):
        self.__next_lang = next_lang

    def set_next_rule_in_chain(self, next_rule):
        self.__next_rule = next_rule

    def pre_check(self, dir_to_check, task_container):
        """
        判断当前语言或架构是否需要进行匹配\n
        默认规则是，排查目标如果已有某语言的任务，则无需匹配\n
        :param dir_to_check: 排查目标
        :param task_container: 任务容器
        :return: 如果需要匹配，则返回True
        """
        return task_container.is_lang_and_dir_had_task(dir_to_check, self.lang_type)

    def process_match(self, dir_to_check, entry_list, task_container):
        """
        每个子类都应视情况重写本方法\n
        查询目录对应的语言和架构，构建CodeQL数据库创建任务的列表\n
        :param dir_to_check:排查目标
        :param entry_list:排查目标下的entry列表（避免重复查询）
        :param task_container:任务容器
        :return:nothing
        """
        pass

    def match(self, dir_to_check, entry_list, task_container):
        """
        语言和架构匹配的责任链模型\n
        :param dir_to_check:排查目标
        :param entry_list:排查目标下的entry列表（避免重复查询）
        :param task_container:任务容器
        :return:nothing
        """
        if self.pre_check(dir_to_check, task_container):
            self.process_match(dir_to_check, entry_list, task_container)
        if self.__next_lang is not None:
            self.__next_lang.is_match(dir_to_check, entry_list, task_container)
        if self.__next_rule is not None:
            self.__next_rule.is_match(dir_to_check, entry_list, task_container)

    @staticmethod
    def build_chain():
        instance = JavaRuleChain()
        return instance
