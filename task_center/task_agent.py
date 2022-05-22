from lang_detector.java_rule import JavaRuleChain
from lang_detector.javascript_rule import JavaScriptRuleChain
from task_center.task import TaskContainer
from utils import config
from utils.util import walk_for_dir_bfs


def build_chain():
    java_rule = JavaRuleChain()
    javascript_rule = JavaScriptRuleChain()

    java_rule.build_chain()
    javascript_rule.build_chain()

    java_rule.set_next_lang_in_chain(javascript_rule)

    return java_rule


class TaskAgent(object):
    def __init__(self):
        self.task_list = list()

    def build_tasks(self, root_dir):
        matcher = build_chain()
        for sub_dir in walk_for_dir_bfs(root_dir, config.lang_detect_depth):
            matcher.match(sub_dir, self.task_list, TaskContainer())
