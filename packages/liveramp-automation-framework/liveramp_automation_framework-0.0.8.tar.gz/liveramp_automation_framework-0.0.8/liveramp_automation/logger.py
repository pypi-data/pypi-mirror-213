# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime
from logging import handlers

log_format = logging.Formatter('%(asctime)s - %(levelname)s - [ %(filename)s: %(lineno)d ] - %(message)s ')

log_path = os.path.join(os.getcwd(), "reports/")
log_name = "{}.log".format(datetime.now().strftime("%Y%m%d%H%M%S"))

Logger = logging.getLogger(log_name)
Logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(log_format)
Logger.addHandler(console_handler)

if not os.path.exists(log_path):
    os.makedirs(log_path)
file_name = "{}/{}".format(log_path, log_name)
file_handler = handlers.TimedRotatingFileHandler(filename=file_name, when='midnight', backupCount=30, encoding='utf-8')
file_handler.setLevel('DEBUG')
file_handler.setFormatter(log_format)
Logger.addHandler(file_handler)

Logger.debug("======Now LOG BEGIN=======")
