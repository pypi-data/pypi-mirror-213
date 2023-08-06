# -*- coding: utf-8 -*-
import random
import schedule
from src.api import FishPi
from .config import GLOBAL_CONFIG
from .redpacket import rush_redpacket


REPEAT_POOL = {}  # 复读池

def init_soliloquize(api: FishPi) -> None:
    if GLOBAL_CONFIG.chat_config.soliloquize_switch:
        schedule.every(GLOBAL_CONFIG.chat_config.soliloquize_frequency).minutes.do(
            soliloquize, api)

def repeat(api: FishPi, msg) -> None:
    if not REPEAT_POOL.__contains__(msg):
        REPEAT_POOL.clear()
        REPEAT_POOL[msg] = 1
    elif REPEAT_POOL[msg] == GLOBAL_CONFIG.chat_config.frequency:
        api.chatroom.send(msg)
        REPEAT_POOL[msg] = REPEAT_POOL[msg] + 1
    else:
        REPEAT_POOL[msg] = REPEAT_POOL[msg] + 1


def soliloquize(api: FishPi) -> None:
    length = len(GLOBAL_CONFIG.chat_config.sentences)
    index = random.randint(0, length - 1)
    api.chatroom.send(GLOBAL_CONFIG.chat_config.sentences[index])

def listener(api: FishPi, message :dict) -> None:
    if message['type'] == 'msg':
        if message['content'].find("redPacket") != -1:
            rush_redpacket(api, message)
        else:
            time = message['time']
            user = message['userName']
            user_nick_name = message['userNickname']
            if len(GLOBAL_CONFIG.chat_config.blacklist) > 0 \
                    and GLOBAL_CONFIG.chat_config.blacklist.__contains__(user):
                return
            if user == GLOBAL_CONFIG.auth_config.username:
                print('\t\t\t\t\t\t[' + time + ']')
                print('\t\t\t\t\t\t你说: ' + message['md'])
            else:
                if 'client' in message:
                    print('[' + time + '] 来自(' + message['client']+')')
                else:
                    print('[' + time + ']')
                if len(user_nick_name) >0:
                    print(f'{user_nick_name}({user})说:')
                else:
                    print(f'{user}说:')    
                print(message['md'])
                print('\r\n')
            if GLOBAL_CONFIG.chat_config.repeat_mode_switch:
                msg = message['md']
                repeat(api, msg)
