class TaskInfo(object):
    def __init__(self):
        self.src_root = None  # 源码目录
        self.lang_type = None  # 语言类型
        self.is_real_task = True  # 是否为需要单独创建数据库和分析的任务，例如Maven工程的子模块就不用单独处理
        self.build_command = None  # 编译Code QL数据库过程中，需要编译的语言应设定此值


class TaskInfoBuilder(object):
    def __init__(self):
        self.task_info = TaskInfo()

    def build(self):
        return self.task_info

    def locate_at(self, src_root):
        self.task_info.src_root = src_root
        return self

    def program_in(self, lang_type):
        self.task_info.lang_type = lang_type
        return self

    def need_separate_analysis(self, is_real_task):
        self.task_info.is_real_task = is_real_task
        return self

    def build_command(self, build_command):
        self.task_info.build_command = build_command
        return self


class TaskContainer(object):
    def __init__(self):
        self.task_dict = {}

    def is_lang_and_dir_had_task(self, src_root, lang_type):
        """
        判断当前目录和语言类型是否已加入任务列表\n
        :param src_root: 源码目录
        :param lang_type: 语言类型
        :return: 如果已有类似任务，则返回True
        """
        return any(task.lang_type is lang_type for task in self.task_dict.get(src_root, []))

    def add_task(self, info):
        if not info or not info.src_root:
            return

        self.task_dict.setdefault(info.src_root, []).append(info)

    def batch_add_task(self, info_arr):
        if not info_arr:
            return

        for info in info_arr:
            self.add_task(info)

    def get_real_tasks(self):
        """
        遍历当前任务容器，取出需要处理的任务\n
        :return: 每次调用返回一个需要处理的任务
        """
        for path in self.task_dict:
            for task in self.task_dict[path]:
                if not task.is_real_task:
                    continue
                yield task

    def __str__(self):
        real_tasks = {}
        virtual_tasks = {}
        for path in self.task_dict:
            for task in self.task_dict[path]:
                tasks = real_tasks if task.is_real_task else virtual_tasks
                tasks[task.lang_type.value] = tasks.get(task.lang_type.value, 0) + 1
        return f'真实任务统计: {real_tasks}, 虚拟任务统计: {virtual_tasks}'
