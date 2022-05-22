from lang_detector.lang_enum import LangType


class Task(object):
    def __init__(self, src_root):
        self.src_root = src_root            # 源码目录
        self.lang_type = LangType.NONE      # 语言类型
        self.is_real_task = True            # 是否为需要单独创建数据库和分析的任务，例如Maven工程的子模块就不用单独处理


class TaskContainer(object):
    def __init__(self):
        self.task_dict = dict()

    def is_lang_and_dir_had_task(self, src_root, lang_type):
        """
        判断当前目录和语言类型是否已加入任务列表\n
        :param src_root: 源码目录
        :param lang_type: 语言类型
        :return: 如果已有类似任务，则返回True
        """
        return any(task.lang_type is lang_type for task in self.task_dict.get(src_root, list()))
