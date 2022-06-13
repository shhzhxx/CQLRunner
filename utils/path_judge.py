import re

from utils import config


class PathJudge(object):
    def __init__(self):
        """
        用于判定给定路径是否被允许参与识别
        """
        self.precedents = []
        for p in config.CONF['lang_detect']['re_excluded_paths']:
            self.precedents.append(re.compile(p))

    def is_guilty(self, path):
        if not self.precedents:
            return False
        for precedent in self.precedents:
            if precedent.search(path):
                return True
        return False
