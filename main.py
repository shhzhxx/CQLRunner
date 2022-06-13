from task_center.task_agent import TaskAgent
from utils import config


def build_local_config():
    # 必须修改
    config.CONF['mvn']['mvn_executable_path'] = r''
    config.CONF['code_ql']['code_ql_executable_path'] = r''
    config.CONF['code_ql']['database']['create']['database_dir'] = r''
    config.CONF['code_ql']['database']['analyze']['output_dir'] = r''
    config.CONF['code_ql']['database']['analyze']['output_postfix'] = ''

    # 可选修改
    config.CONF['log_file_path'] = r''


if __name__ == '__main__':
    build_local_config()
    task_agent = TaskAgent(r'')
    task_agent.build_tasks()
