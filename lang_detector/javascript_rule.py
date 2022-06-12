import os.path

from lang_detector.lang_enum import LangType
from lang_detector.lang_matcher import LangMatcher
from task_center.task import TaskInfoBuilder


class JavaScriptRuleChain(LangMatcher):
    def __init__(self):
        super().__init__()
        self.lang_type = LangType.JAVASCRIPT

    def build_chain(self):
        electron_rule = ElectronRule()
        vue_rule = VueRule()
        angular_rule = AngularRule()

        electron_rule.set_next_rule_in_chain(vue_rule)
        vue_rule.set_next_rule_in_chain(angular_rule)
        self.set_next_rule_in_chain(electron_rule)

    @staticmethod
    def simple_match(dir_to_check, entry_list, task_container, dep_file_name, key_word):
        """
        常见的宽松检查，目标文件中存在目标关键字时，即认为匹配\n
        """
        if dep_file_name not in entry_list:
            return
        is_matched = False
        with open(os.path.join(dir_to_check, dep_file_name), 'r', encoding='utf=8') as f:
            for line in f.readlines():
                if key_word in line:
                    is_matched = True
                    break
        if is_matched:
            task_info = TaskInfoBuilder() \
                .locate_at(dir_to_check) \
                .program_in(LangType.JAVASCRIPT) \
                .build()
            task_container.add_task(task_info)


class ElectronRule(JavaScriptRuleChain):
    def __init__(self):
        """
        当前规则比较宽松，目录下存在package.json文件，且存在字符串"electron"即可
        """
        super().__init__()
        self.key_word = '"electron"'
        self.dep_file_name = 'package.json'

    def process_match(self, dir_to_check, entry_list, task_container):
        JavaScriptRuleChain.simple_match(dir_to_check, entry_list, task_container, self.dep_file_name, self.key_word)


class VueRule(JavaScriptRuleChain):
    def __init__(self):
        """
        当前规则比较宽松，目录下存在package.json文件，且存在字符串"vue"即可
        """
        super().__init__()
        self.key_word = '"vue"'
        self.dep_file_name = 'package.json'

    def process_match(self, dir_to_check, entry_list, task_container):
        JavaScriptRuleChain.simple_match(dir_to_check, entry_list, task_container, self.dep_file_name, self.key_word)


class AngularRule(JavaScriptRuleChain):
    def __init__(self):
        """
        当前规则比较宽松，目录下存在package.json文件，且存在字符串"@angular即可
        """
        super().__init__()
        self.key_word = '"@angular'
        self.dep_file_name = 'package.json'

    def process_match(self, dir_to_check, entry_list, task_container):
        JavaScriptRuleChain.simple_match(dir_to_check, entry_list, task_container, self.dep_file_name, self.key_word)
