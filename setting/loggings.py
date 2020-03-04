#-*- coding:utf-8 -*-  
""" 
Author:hel 
License: Apache Licence 
File: loggings.py 
Time: 2019/10/24
Version: 1.0
@Function: 处理日志
"""

import logging
import logging.handlers
import os

if os.path.exists('/root/logs/'):
    logging_file_dir = '/root/logs/'
else:
    os.mkdir('/root/logs/')


def create_logger():
    """
    设置日志
    :param app:
    :return:
    """


    # app日志打印
    trace_file_handler = logging.FileHandler(
        os.path.join(logging_file_dir, 'app.log')
    )
    trace_file_handler.setFormatter(logging.Formatter('%(message)s'))
    log_trace = logging.getLogger('app')
    log_trace.addHandler(trace_file_handler)
    log_trace.setLevel(logging.INFO)