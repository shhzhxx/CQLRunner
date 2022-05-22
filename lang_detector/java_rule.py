from lang_detector.lang_enum import LangType
from lang_detector.lang_matcher import LangMatcher


class JavaRuleChain(LangMatcher):
    def __init__(self):
        super().__init__()
        self.lang_type = LangType.JAVA
        self.build_chain()

    def build_chain(self):
        maven_rule = MavenRule()
        gradle_rule = GradleRule()

        maven_rule.set_next_rule_in_chain(gradle_rule)
        self.set_next_rule_in_chain(maven_rule)


class MavenRule(JavaRuleChain):
    def __init__(self):
        super().__init__()
        self.checked_dir_set = set()

    def is_match(self, dir_to_check, task_list):
        pass


class GradleRule(JavaRuleChain):
    def is_match(self, dir_to_check, task_list):
        pass
