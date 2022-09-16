import base64
import configparser
import os
import re
import datetime

import requests

onLoadUrl = 'http://10.1.1.10/'
connectUrl = 'http://10.1.1.10:801/eportal/portal/custom/auth'

base_dir = os.path.dirname(os.path.abspath(__file__))
userConfig = configparser.ConfigParser()
userConfig.read(base_dir + '/config.ini')
user_name = userConfig.get('user', 'account')
user_passwd = userConfig.get('user', 'password')

run_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")


def connect():
    try:
        load_page = requests.get(onLoadUrl)
        if re.findall("<title>上网登录页</title>", load_page.text):
            user_ip = re.findall("v46ip='(.+?)'", load_page.text)

            params = {
                'user_account': user_name,
                'user_password': base64.b64encode(user_passwd.encode("utf-8")),
                'wlan_user_ip': user_ip[0],
                'wlan_user_mac': '',
                'type': '1',
                'lang': ''
            }

            on_connect = requests.get(connectUrl, params)
            if re.findall('"result":1', on_connect.text):
                print("connect succeed")
                return 0
            else:
                print("connect failed")
                return -1

        else:
            print("already connected")
            return 0

    except:
        return -1


if __name__ == "__main__":
    if connect() != 0:
        errLog = open("error.log", "a+")
        errLog.write(run_time + '\n' + 'Connection failure')
        errLog.close()
        exit(-1)

