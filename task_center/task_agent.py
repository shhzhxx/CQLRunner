from lang_detector.lang_matcher import LangMatcher
from utils import config
from utils.util import walk_for_dir_bfs


class TaskAgent(object):
    def __init__(self):
        self.task_list = list()

    def build_tasks(self, root_dir):
        matcher = LangMatcher.build_chain()
        for sub_dir in walk_for_dir_bfs(root_dir, config.lang_detect_depth):
            matcher.is_match(sub_dir, self.task_list)
