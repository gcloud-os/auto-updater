#encoding=utf-8

'''
Created on Jul 28, 2015

@author: kongmq
'''

import ConfigParser
import argparse

DEFAULT_CONFIG_PATH = '/etc/gcloud/updater.conf'


class _cfg(object):
    """class for config."""

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst = super(_cfg, cls).__new__(cls, *args, **kwargs)

            cf = ConfigParser.ConfigParser()
            if "config" in kwargs:
                cf.read(kwargs.get("config"))
            else:
                cf.read(DEFAULT_CONFIG_PATH)

            sections = cf.sections()
            for section in sections:
                options = cf.options(section)
                option_dict = {}
                for option in options:
                    option_dict[option] = cf.get(section, option)
                setattr(cls._inst, section, option_dict)

        return cls._inst

CONF = _cfg()


