import os
import shutil
import subprocess

from lang_detector.java_rule import JavaRuleChain
from lang_detector.javascript_rule import JavaScriptRuleChain
from task_center.task import TaskContainer
from utils import config
from utils.path_judge import PathJudge
from utils.util import walk_for_dir_bfs


def build_chain():
    """
    构建项目语言分析的责任链，如果有新增规则，这里应同步修改\n
    :return:
    """
    java_rule = JavaRuleChain()
    javascript_rule = JavaScriptRuleChain()

    java_rule.build_chain()
    javascript_rule.build_chain()

    java_rule.set_next_lang_in_chain(javascript_rule)

    return java_rule


def database_create(task_info):
    """
    构建并执行Code QL的创建数据库指令\n
    :param task_info:
    :return:
    """
    command_list = list()
    command_list.append(config.CONF['code_ql']['code_ql_executable_path'])
    command_list.append('database')
    command_list.append('create')
    # [OPTIONS]
    command_list.extend(config.CONF['code_ql']['database']['create']['other_options'])
    command_list.append(f'--language={task_info.lang_type.value}')
    command_list.append(f'--source-root={task_info.src_root}')
    command_list.append(f'--command={task_info.build_command(task_info)}') if task_info.build_command else None
    # 分隔符
    command_list.append('--')
    # <database>: <database_dir>/java_demo
    command_list.append(os.path.join(config.CONF['code_ql']['database']['create']['database_dir'],
                                     f'{task_info.lang_type.value}_{os.path.basename(task_info.src_root)}'))
    with subprocess.Popen(command_list,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          encoding="utf-8") as p:
        for line in p.stdout:
            print(line, end='')


def database_analyze(task_info):
    """
    构建并执行Code QL的分析数据库指令\n
    :param task_info:
    :return:
    """
    command_list = list()
    command_list.append(config.CONF['code_ql']['code_ql_executable_path'])
    command_list.append('database')
    command_list.append('analyze')
    # [OPTIONS]
    command_list.extend(config.CONF['code_ql']['database']['analyze']['other_options'])
    command_list.append(f'--format={config.CONF["code_ql"]["database"]["analyze"]["format"]}')
    command_list.append(f'''--output={os.path.join(config.CONF['code_ql']['database']['analyze']['output_dir'],
                                                   f'{task_info.lang_type.value}_'
                                                   f'{os.path.basename(task_info.src_root)}.'
                                                   f'{config.CONF["code_ql"]["database"]["analyze"]["output_postfix"]}'
                                                   )}''')
    # 分隔符
    command_list.append('--')
    # <database>: <database_dir>/java_demo
    command_list.append(os.path.join(config.CONF['code_ql']['database']['create']['database_dir'],
                                     '_'.join([task_info.lang_type.value, os.path.basename(task_info.src_root)])))
    command_list.append(config.CONF['code_ql']['database']['analyze']['queries_to_execute'][task_info.lang_type.value])
    with subprocess.Popen(command_list,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          encoding="utf-8") as p:
        for line in p.stdout:
            print(line, end='')


def clear_dir(target):
    """
    删除目标目录并重建\n
    :param target: 目标目录
    :return:
    """
    print(f'正在清空目录：{target}')
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)


def preprocess():
    """
    根据配置进行运行前的处理，目前是清空一些最好为空的目录\n
    :return:
    """
    if not config.CONF['rmtree_before_use']:
        return
    clear_dir(config.CONF['code_ql']['database']['create']['database_dir'])
    clear_dir(config.CONF['code_ql']['database']['analyze']['output_dir'])


class TaskAgent(object):
    def __init__(self):
        self.root_dir = None
        self.task_container = TaskContainer()
        self.path_judge = PathJudge()

    def locate_at(self, root_dir):
        self.root_dir = root_dir
        return self

    def build_tasks(self):
        print('开始预处理')
        preprocess()
        print('结束预处理')
        print('开始构建分析链')
        matcher = build_chain()
        print('结束构建分析链')
        print('开始分析目录')
        for sub_dir in walk_for_dir_bfs(self.root_dir, config.CONF['lang_detect']['depth']):
            if self.path_judge.is_guilty(sub_dir):
                continue
            matcher.match(sub_dir, os.listdir(sub_dir), self.task_container)
        print('结束分析目录')
        print('开始构建Code QL数据库')
        for task in self.task_container.get_real_tasks():
            print(f'开始构建Code QL数据库，目标为{task.src_root}')
            database_create(task)
        print('结束构建Code QL数据库')
        print('开始运行规则')
        for task in self.task_container.get_real_tasks():
            print(f'开始运行规则，目标为{task.src_root}')
            database_analyze(task)
        print('结束运行规则')
