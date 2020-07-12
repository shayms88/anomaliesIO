import os
import errno
import logging
import logging.handlers as handlers
import platform
import __main__
from datetime import datetime
from os.path import basename

UNIX_LOG_PATH = '/tmp/log_files/'


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _make_log_dir():
    mkdir_p(UNIX_LOG_PATH)


def _get_formatter():
    return logging.Formatter('%(asctime)s ^ %(name)s ^ %(levelname)s ^ %(threadName)s ^ %(message)s')


class Log(object):

    instance = None

    def __init__(self, module_name, file_name=None):

        self._module_name = module_name

        try:
            if not Log.instance:
                Log.instance = True
                self._create_root_logger()
                self._add_handlers()

            self.logger = logging.getLogger(self._module_name)

        except Exception as e:
            print("{timestamp} Fatal error. couldn't create logger: {error_msg} - ".format(
                timestamp=datetime.utcnow(),
                error_msg=str(e)))

    def _create_root_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def _add_handlers(self):
        # screen handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(_get_formatter())
        self.logger.addHandler(ch)

        # file handler
        _make_log_dir()
        platform_log_path = UNIX_LOG_PATH
        log_file_name = basename(__main__.__file__)
        date_postfix = datetime.today().strftime('%Y%m%d')
        log_path = platform_log_path + log_file_name + '_' + date_postfix + '.log'
        fh = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=14)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(_get_formatter())
        self.logger.addHandler(fh)

    def log_warning(self, message):
        self.logger.warning('{message}'.format(message=message))

    def log_info(self, message):
        self.logger.info('{message}'.format(message=message))

    def log_error(self, message):
        self.logger.error('{message}'.format(message=message))

    def log_debug(self, message):
        self.logger.debug('{message}'.format(message=message))

    def log_critical(self, message):
        self.logger.critical(message)
