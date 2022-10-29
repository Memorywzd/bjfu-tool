import configparser
import os

import requests

from notify import send_message

base_dir = os.path.dirname(os.path.abspath(__file__))
billConfig = configparser.ConfigParser()
billConfig.read(base_dir + '/config.ini')
eAccount = billConfig.get('ebill', 'account')
ePasswd = billConfig.get('ebill', 'password')
building = billConfig.get('ebill', 'building')
floor = billConfig.get('ebill', 'floor')
room = billConfig.get('ebill', 'room')
room_id = billConfig.get('ebill', 'room_id')


class ElectricityBill:
    def __init__(self):
        self.total, self.free, self.used, self.remain = '', '', '', ''
        self.date = ''
        self.status = 0


def get_remain_value():
    loginUrl = 'http://pay.bjfu.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action'
    queryUrl = 'http://pay.bjfu.edu.cn/MNetWorkUI/elecManage!querySydlOfE028'
    if room_id == '':
        get_room_id = ''

    s = requests.sessions.Session()

    login_data = {
        'nickName': eAccount,
        'password': ePasswd,
    }
    s.post(url=loginUrl, data=login_data)

    query_data = {
        'factorycode': 'E028',
        'roomid': room_id
    }

    eb = ElectricityBill()
    value = s.post(url=queryUrl, data=query_data)
    if value.status_code != 200:
        eb.status = -1
    data = value.json()
    eb.total, eb.free, eb.used, eb.remain = data.get('totalEq'), data.get('freeEq'), data.get('useEq'), data.get(
        'remainEq')
    eb.date = data.get('updateDt')
    return eb


if __name__ == '__main__':
    eq = get_remain_value()
    ebill_message = '电费监测脚本：' + '\n'
    if eq.status == -1:
        ebill_message += '访问电费监控接口失败'
        send_message(ebill_message)
    else:
        if float(eq.remain) <= 20:
            ebill_message += '截至' + eq.date + '\n剩余' + eq.remain + '度电，电费已不足20度，请尽快缴费！'
            send_message(ebill_message)
