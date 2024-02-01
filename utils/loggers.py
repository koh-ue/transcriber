#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: FIXME: XXX: HACK: NOTE: INTENT: USAGE:

import os
import yaml
from colors import *
from logging import getLogger, config

class Log:
    def __init__(self, name, file, no_file, config_file="src/library/misc/log-config.yaml") -> None:
        print(__file__)
        with open(config_file, 'r') as f:
            self.log_conf = yaml.safe_load(f)
        self.log_conf["formatters"]["stdout"]["format"] = PURPLE+"%(asctime)s " + BLUE+"%(name)s:%(lineno)s "+"%(funcName)s " + BOLD_YELLOW+"[%(levelname)s]: "+END+"%(message)s"
        if no_file:
            del self.log_conf["handlers"]["fileHandler"]
            for each_logger in ["__main__", "same_hierarchy", "lower.sub"]:
                self.log_conf["loggers"][each_logger]["handlers"] = ["consoleHandler"]
        else:
            self.log_conf["handlers"]["fileHandler"]["filename"] = f"{os.path.dirname(file)}/logs/{os.path.splitext(os.path.basename(file))[0]}.log"
            os.makedirs(os.path.dirname(self.log_conf["handlers"]["fileHandler"]["filename"]), exist_ok=True)
        config.dictConfig(self.log_conf)
        self.logger = getLogger(name)