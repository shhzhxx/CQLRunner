import re
from os import scandir
from os.path import isdir, abspath

from utils import config


def walk_for_dir_bfs(root_dir, depth):
    """
    宽度优先遍历目标路径下的目录，有深度限制\n
    :param root_dir: 需要遍历的根目录
    :param depth: 遍历深度
    :return: 目标路径下的目录(包括传入的根目录)
    """
    if isdir(root_dir) and depth > -1:
        yield abspath(root_dir)
    else:
        return None
    yield from __walk_for_dir_bfs_core(root_dir, depth)


def __walk_for_dir_bfs_core(root_dir, depth):
    if depth > 0:
        for entry in scandir(root_dir):
            if entry.is_dir():
                yield entry.path
                yield from __walk_for_dir_bfs_core(entry.path, depth - 1)


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
