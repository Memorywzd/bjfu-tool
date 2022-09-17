import configparser
import datetime

import requests

botConfig = configparser.ConfigParser()
botConfig.read('config.ini')
bot_url = botConfig.get('qqbot', 'bot_url')
bot_message_type = botConfig.get('qqbot', 'message_type')
send_to = botConfig.get('qqbot', 'qq_id')


def send_message(message):
    try:
        user_id = ''
        group_id = ''
        if bot_message_type == 'private':
            user_id = send_to
        elif bot_message_type == 'group':
            group_id = send_to

        send_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
        message = send_time + '\n' + message

        params = {
            'message_type': bot_message_type,
            'user_id': user_id,
            'group_id': group_id,
            'message': message
        }
        on_send_message = requests.post(url=bot_url, data=params)
        response_data = on_send_message.json()
        if response_data.get('status') == 'ok':
            print("message send")
            return 0
        else:
            return -1

    except:
        return -1
