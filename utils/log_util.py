import logging


class EasyLogFactory(object):
    @staticmethod
    def produce(logger_name, log_file_path, file_level=logging.INFO, console_level=logging.DEBUG):
        if log_file_path:
            return EasyLogFactory.__console_and_file(logger_name, log_file_path, file_level, console_level)
        else:
            return EasyLogFactory.__console(logger_name, console_level)

    @staticmethod
    def __console(logger_name, console_level):
        logging.basicConfig(
            format='[%(asctime)s] - %(name)s - %(message)s',
            level=console_level
        )

        return logging.getLogger(logger_name)

    @staticmethod
    def __console_and_file(logger_name, log_file_path, file_level, console_level):
        # set up logging to file
        logging.basicConfig(
            filename=log_file_path,
            level=file_level,
            encoding='utf-8',
            format='[%(asctime)s] - %(name)s - %(message)s',
        )

        # set up logging to console
        console = logging.StreamHandler()
        console.setLevel(console_level)
        # set a format which is simpler for console use
        formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger(logger_name).addHandler(console)

        return logging.getLogger(logger_name)
