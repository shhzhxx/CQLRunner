from lang_detector.lang_enum import LangType
from lang_detector.lang_matcher import LangMatcher


class JavaScriptRuleChain(LangMatcher):
    def __init__(self):
        super().__init__()
        self.lang_type = LangType.JAVASCRIPT
        self.build_chain()

    def build_chain(self):
        electron_rule = ElectronRule()
        self.set_next_rule_in_chain(electron_rule)


class ElectronRule(JavaScriptRuleChain):
    def __init__(self):
        super().__init__()

    def process_match(self, dir_to_check, entry_list, task_container):
        pass
