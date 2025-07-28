# -*- coding: utf-8 -*-
# @Time    : 2021/4/28 14:20
# @Author  : Joshua
# @File    : settings

import logging.config
import os
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG位置
API_LOG_DIR = '/data/JST_API/'
# 测试地址

USER_AGENT = [
    #win7
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',

    #win10
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
]

# js_server 地址
# NODEJS_SERVER = 'http://xxxxxxxxxx:3000'  # 本地
# NODEJS_SERVER = 'http://localhost:3000'  # 本地
NODEJS_SERVER = 'http://xxxxxxxxxx.cn/spider'  # spider


if platform.system() == 'Windows':
    TESTING = True
    LOCAL_TESTING = True
    LOG_DIR = '/'.join([BASE_DIR, '/log'])
elif platform.system() == 'Linux':
    TESTING = False
    LOCAL_TESTING = False
    LOG_DIR = '/'.join([API_LOG_DIR, '/log'])

TESTING = False
MAX_UV = 100
SHOP_NAME = '茵曼旗舰店'
DOWNLOAD_DIR = '/'.join([BASE_DIR, '/生意参谋直播数据'])

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
        # 日志格式
    },
    'encoding': 'utf-8',
    'filters': {
    },
    'handlers': {
        # 'default': {
        #     'level':'DEBUG',
        #     'class':'logging.handlers.RotatingFileHandler',
        #     'filename': '//'.join([LOG_DIR, 'default.log']),     #日志输出文件
        #     'maxBytes': 1024*1024*5,                  #文件大小
        #     'backupCount': 5,                         #备份份数
        #     'formatter':'standard',                   #使用哪种formatters日志格式
        # },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '//'.join([LOG_DIR, 'error.log']),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 按文件大小
            'filename': '//'.join([LOG_DIR, 'info.log']),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'SycmFlow': {'handlers': ['console', 'error', 'info'],
                     'level': 'INFO',
                     'propagate': True}
    }
}
logging.config.dictConfig(LOGGING)
