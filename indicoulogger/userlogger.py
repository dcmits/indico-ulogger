import logging

from indico.core.config import Config


class MaxLevelFilter(logging.Filter):
    '''Filters (lets through) all messages with level < LEVEL'''
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level # "<" instead of "<=": since logger.setLevel is inclusive, this should be exclusive


class UserLogger():

    def __init__(self):
        # create LOGGER
        self.logger = None
        MIN_LEVEL= logging.INFO
        config = Config.getInstance()
        configLogDir = config.getLogDir()
        logFilePath_info = configLogDir + "/user_logger.log"

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - user-logger - %(levelname)s - %(message)s')
        self.logger.setLevel(MIN_LEVEL)
        stdout_hdlr = logging.handlers.TimedRotatingFileHandler(filename=logFilePath_info, encoding='utf8', when='W6',
                                                                backupCount=0)
        lower_than_warning = MaxLevelFilter(logging.WARNING)
        stdout_hdlr.addFilter( lower_than_warning )     #messages lower than WARNING go to stdout
        stdout_hdlr.setFormatter(formatter)
        stdout_hdlr.setLevel( MIN_LEVEL )
        self.logger.addHandler(stdout_hdlr)
