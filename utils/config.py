# 根据规则匹配出的语言类型集合
detected_lang_set = set()

CONF = {
    # 对于对一些不能非空的操作目录，使用前预先清空，例如数据库目录
    'rmtree_before_use': False,
    'lang_detect': {
        # 对给定的目录进行探测的深度
        'depth': 2
    },
    'mvn': {
        # 【必须修改】maven可执行文件路径
        'mvn_executable_path': None,
        # maven执行时的一些全局选项
        'options': ['--batch-mode', '--fail-never', '--quiet', '-U'],
        # maven操作时的线程数
        'threads': '4',
        # maven的settings.xml配置文件路径
        'settings': None,
        # maven执行时的系统属性
        'defines': [
            # # disable SSL verification
            # 'maven.wagon.http.ssl.insecure=true',
            # 'maven.wagon.http.ssl.allowall=true',
            # 'maven.wagon.http.ssl.ignore.validity.dates=true',
            # # disable test
            'maven.test.skip=true'
        ],
        # maven需要执行的phase
        'phase': ['clean', 'compile'],
    },
    'code_ql': {
        # 【必须修改】code_ql可执行文件路径
        'code_ql_executable_path': None,
        'database': {
            # 详情请参考codeql database create --help -v的说明
            'create': {
                # 【必须修改】所有数据库的根目录
                'database_dir': None,
                # 如果有其它想自定义的选项，可以填到这里
                'other_options': ['--threads=4',
                                  '--overwrite',
                                  '--no-count-lines'],
            },
            # 详情请参考codeql database analyze --help -v的说明
            'analyze': {
                # 结果输出的格式
                'format': 'csv',
                # 【必须修改】所有结果的根目录
                'output_dir': None,
                # 【必须修改】所有结果文件的后缀
                'output_postfix': None,
                'queries_to_execute': {
                    # 需要执行的<query|dir|suite|pack>，新增语言识别或自定义查询规则后应更新这里
                    'java': 'java-security-extended',
                    'javascript': 'javascript-security-extended'
                },
                # 如果有其它想自定义的选项，可以填到这里
                'other_options': ['--threads=4'],
            }
        }
    }
}
