from task_center.task_agent import TaskAgent
from utils import config


def build_local_config():
    config.CONF['mvn']['mvn_executable_path'] = r''
    config.CONF['code_ql']['code_ql_executable_path'] = r''
    config.CONF['code_ql']['database']['create']['database_dir'] = r''
    config.CONF['code_ql']['database']['analyze']['output_dir'] = r''
    config.CONF['code_ql']['database']['analyze']['output_postfix'] = ''


if __name__ == '__main__':
    build_local_config()
    task_agent = TaskAgent()
    task_agent.locate_at(r'').build_tasks()
