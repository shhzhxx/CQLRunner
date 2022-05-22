# 根据规则匹配出的语言类型集合
detected_lang_set = set()

CONF = {
    'lang_detect': {
        'depth': 2  # 对给定的目录进行探测的深度
    },
    'mvn': {
        'mvn_executable_path': None,
        'options': ['--batch-mode', '--fail-never', '--quite'],
        'threads': '4',
        'settings': None,
        'defines': [
            # disable SSL verification
            # 'maven.wagon.http.ssl.insecure=true',
            # 'maven.wagon.http.ssl.allowall=true',
            # 'maven.wagon.http.ssl.ignore.validity.dates=true',
            # disable test
            'maven.test.skip=true'
        ],
        'phase': ['clean', 'compile']
    }
}
