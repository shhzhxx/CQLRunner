from lang_detector.lang_enum import LangType
from lang_detector.lang_matcher import LangMatcher
from utils import config
from functools import reduce
from os import path


class JavaRuleChain(LangMatcher):
    def __init__(self):
        super().__init__()
        self.lang_type = LangType.JAVA

    def build_chain(self):
        maven_rule = MavenRule()
        gradle_rule = GradleRule()

        maven_rule.set_next_rule_in_chain(gradle_rule)
        self.set_next_rule_in_chain(maven_rule)


class MavenRule(JavaRuleChain):
    def __init__(self):
        super().__init__()
        self.checked_dir_set = {0} - {0}
        self.command_build_method = MavenRule.build_command

    def process_match(self, dir_to_check, entry_list, task_container):
        pass

    @staticmethod
    def build_command(src_root):
        command_list = list()
        command_list.append(config.CONF['mvn']['mvn_executable_path'] or 'mvn')
        command_list.extend(config.CONF['mvn']['options'] or [])
        command_list.extend(reduce(list.__add__, [['--define', arg] for arg in config.CONF['mvn']['defines']])) if \
            config.CONF['mvn']['defines'] else None
        command_list.extend(['--file', path.join(src_root, 'pom.xml')])
        command_list.extend(['--settings', config.CONF['mvn']['settings']]) if config.CONF['mvn']['settings'] else None
        command_list.extend(['--threads', config.CONF['mvn']['threads']]) if config.CONF['mvn']['threads'] else None
        command_list.extend(config.CONF['mvn']['phase'] or [])
        return ' '.join([i if ' ' in i else f'"f{i}"' for i in command_list])


class GradleRule(JavaRuleChain):
    def process_match(self, dir_to_check, entry_list, task_container):
        pass
