import os
import shutil
import subprocess

from lang_detector.java_rule import JavaRuleChain
from lang_detector.javascript_rule import JavaScriptRuleChain
from task_center.task import TaskContainer
from utils import config
from utils.log_util import EasyLogFactory
from utils.path_util import PathJudge
from utils.path_util import walk_for_dir_bfs


class TaskAgent(object):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.task_container = TaskContainer()
        self.path_judge = PathJudge()
        self.logger = EasyLogFactory.produce('task_agent', config.CONF['log_file_path'])

    def run_command(self, command_list):
        with subprocess.Popen(command_list,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              encoding="utf-8") as p:
            for line in p.stdout:
                self.logger.warning(line.strip())

    def build_tasks(self):
        # 预处理
        self.preprocess()

        # 构建分析链
        matcher = self.build_chain()

        # 分析目录，识别任务
        self.logger.debug('开始分析目录')
        for sub_dir in walk_for_dir_bfs(self.root_dir, config.CONF['lang_detect']['depth']):
            if self.path_judge.is_guilty(sub_dir):
                self.logger.info(f'目录被忽略，路径为{sub_dir}')
                continue
            matcher.match(sub_dir, os.listdir(sub_dir), self.task_container)
        self.logger.debug(self.task_container)

        # 构建Code QL数据库
        self.logger.debug('开始构建Code QL数据库')
        for task in self.task_container.get_real_tasks():
            self.logger.debug(f'开始构建Code QL数据库，目标为{task.src_root}')
            self.database_create(task)

        # 运行规则
        self.logger.debug('开始运行规则')
        for task in self.task_container.get_real_tasks():
            self.logger.debug(f'开始运行规则，目标为{task.src_root}')
            self.database_analyze(task)

    def preprocess(self):
        """
        根据配置进行运行前的处理，目前是清空过程中产生的目录和文件，例如数据库目录、结果目录、日志文件\n
        :return:
        """
        self.logger.debug('开始预处理')
        if not config.CONF['rmtree_before_use']:
            return
        self.clear_path(config.CONF['code_ql']['database']['create']['database_dir'])
        self.clear_path(config.CONF['code_ql']['database']['analyze']['output_dir'])
        self.clear_path(config.CONF['log_file_path'])

    def clear_path(self, target):
        """
        如果目标是目录，删除并重建\n
        如果目标是文件，删除\n
        如果目标不存在，直接返回\n
        :param target: 目标目录
        :return:
        """
        if not os.path.exists(target):
            return
        if os.path.isdir(target):
            self.logger.debug(f'正在清空目录{target}')
            shutil.rmtree(target)
            os.mkdir(target)
            return
        if os.path.isfile(target):
            self.logger.debug(f'正在删除文件{target}')
            os.remove(target)

    def build_chain(self):
        """
        构建项目语言分析的责任链，如果有新增规则，这里应同步修改\n
        :return:
        """
        self.logger.debug('开始构建分析链')
        java_rule = JavaRuleChain()
        javascript_rule = JavaScriptRuleChain()

        java_rule.build_chain()
        javascript_rule.build_chain()

        java_rule.set_next_lang_in_chain(javascript_rule)

        return java_rule

    def database_create(self, task_info):
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
        self.run_command(command_list)

    def database_analyze(self, task_info):
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
        command_list.append(
            config.CONF['code_ql']['database']['analyze']['queries_to_execute'][task_info.lang_type.value])
        self.run_command(command_list)
