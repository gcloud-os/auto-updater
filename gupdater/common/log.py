#coding=utf-8
#!/usr/bin/python

'''
Created on Jul 27, 2015

@author: kongmq
'''

from .conf import CONF

import logging
import os

PATH = CONF.GENERAL.get('log', '/var/log/gupdater/')
FORMATTER = '[ %(asctime)s - %(name)s - %(levelname)s ] %(message)s'
# LOG_LEVEL = logging._levelNames[CONF.default.get('log_level', 'DEBUG')]

_LOGGER = {

}


class Logger(object):
    """class for log."""

    def __init__(self, name='updater.log',
                 level=logging.DEBUG, formatter=FORMATTER,
                 file_out=True, stream_out=True):

        self.name = name
        if name in _LOGGER:
            return

        if not os.path.exists(PATH):
            os.makedirs(name=PATH)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        file_name = os.path.join(PATH, name)
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)

        log_formatter = logging.Formatter(formatter)
        file_handler.setFormatter(log_formatter)
        stream_handler.setFormatter(log_formatter)

        if file_out:
            self.logger.addHandler(file_handler)

        if stream_out:
            self.logger.addHandler(stream_handler)

        _LOGGER[name] = self.logger

    def getLogger(self):
        return _LOGGER[self.name]

    def _set_level(self, level):
        self.logger.setLevel(level)

'''
LOG = Logger(name='test', level=logging.DEBUG).getLogger()
LOG.warn('warn')
LOG.debug('debug')
LOG.info('info')
LOG.error('error')
'''
