import requests
import os
import json
import time
import sys
from dotenv import load_dotenv
load_dotenv()


class Debugger(object):
    """
        Class for debugger print
    """

    def __init__(self):
        pass

    @staticmethod
    def error_print(msg, debug=True):
        if debug:
            print('[error]' + msg)

    @staticmethod
    def warn_print(msg, debug=True):
        if debug:
            print('[warning]' + msg)

    @staticmethod
    def debug_print(msg, debug=True):
        if debug:
            print('[debug]' + msg + '\r', end='')
            sys.stdout.flush()

    @staticmethod
    def info_print(msg):
        print('[info]' + msg)

    @staticmethod
    def time_print(msg, begin, profiling=False):
        if profiling:
            assert isinstance(begin, type(time.time())
                              ), 'invalid begin time {}'.format(begin)
            print('[info]{}, elapsed for {:.2f}s'.format(
                msg, time.time() - begin))

    @staticmethod
    def dc_print(msg, debug=True):
        data = {
            'content': msg
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(os.getenv('DC_WEBHOOK'),
                                 data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            print("訊息已成功發送到Discord Webhook！")
        else:
            print("發送訊息到Discord Webhook時出現錯誤！")
