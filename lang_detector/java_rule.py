import os.path
from functools import reduce
from os import path
from xml.etree import ElementTree as eTree

from lang_detector.lang_enum import LangType
from lang_detector.lang_matcher import LangMatcher
from task_center.task import TaskInfoBuilder
from utils import config


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
        """
        当前规则是，目录下存在pom.xml文件即可，但是由父级pom定义的模块不会被重复分析
        """
        super().__init__()
        self.command_build_method = MavenRule.build_command
        self.pom_file_name = 'pom.xml'

    def process_match(self, dir_to_check, entry_list, task_container):
        if self.pom_file_name not in entry_list:
            return

        tasks = []
        try:
            tasks = self.recursive_parse_pom(dir_to_check, True)
        except BaseException as e:
            print(e)

        task_container.batch_add_task(tasks)

    def recursive_parse_pom(self, cur_dir, is_real_task):
        """
        递归解析Maven项目的模块与子孙模块\n
        :param cur_dir: 当前要解析的目录，注意，该目录下必须存在正常的pom文件，否则会抛出异常
        :param is_real_task: 用于配置TaskInfo，子模块不重复分析
        :return: TaskInfo列表
        """
        tasks = list()
        parent_task_info = TaskInfoBuilder() \
            .locate_at(cur_dir) \
            .program_in(self.lang_type) \
            .need_separate_analysis(is_real_task) \
            .build_command(MavenRule.build_command) \
            .build()
        tasks.append(parent_task_info)

        pom = eTree.parse(os.path.join(cur_dir, self.pom_file_name))
        namespaces = {'ns': 'http://maven.apache.org/POM/4.0.0'}
        modules = pom.findall('./ns:modules/ns:module', namespaces=namespaces)

        for module in modules:
            child_tasks = self.recursive_parse_pom(os.path.join(cur_dir, module.text), False)
            tasks.extend(child_tasks)
        return tasks

    @staticmethod
    def build_command(task_info):
        command_list = list()
        command_list.append(config.CONF['mvn']['mvn_executable_path'])
        command_list.extend(config.CONF['mvn']['options'] or [])
        command_list.extend(reduce(list.__add__, [['--define', arg] for arg in config.CONF['mvn']['defines']])) if \
            config.CONF['mvn']['defines'] else None
        command_list.extend(['--file', path.join(task_info.src_root, 'pom.xml')])
        command_list.extend(['--settings', config.CONF['mvn']['settings']]) if config.CONF['mvn']['settings'] else None
        command_list.extend(['--threads', config.CONF['mvn']['threads']]) if config.CONF['mvn']['threads'] else None
        command_list.extend(config.CONF['mvn']['phase'] or [])
        return ' '.join(command_list)


class GradleRule(JavaRuleChain):
    def process_match(self, dir_to_check, entry_list, task_container):
        pass
