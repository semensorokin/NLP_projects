# -*- coding: utf-8 -*-

import urllib2 as url
import json
import time
import http_request_introduction as net
import re
import news_api as news_api
from HTMLParser import HTMLParser

BASE_URL = 'api.vk.com/method'
ACCESS_TOKEN = '???'
API_VERSION = 5.52

SEND_MESSAGE_COMMAND = 'messages.send'
GET_MESSAGES_COMMAND = 'messages.get'
GET_MESSAGES_HISTORY_COMMAND = 'messages.getHistory'
GET_USER_COMMAND = 'users.get'

USER_ID = 432264122
CHAT_ID = 78
PEER_ID = USER_ID
# PEER_ID = 2000000000 + CHAT_ID

LOAD_COUNT = 50

USER_ID_PARAM = {
    'user_id': USER_ID,
}

CHAT_ID_PARAM = {
    'chat_id': CHAT_ID,
}

# DIALOG_PARAM = CHAT_ID_PARAM
DIALOG_PARAM = USER_ID_PARAM



last_seen_message = None

uid_to_messages = {}

def execute_in_vk(method, params={}):
    p = params
    p.update({
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION
    })
    address = net.construct_https_url(BASE_URL,
                            path=method,
                            params=p)

    res = url.urlopen(address).read()
    return res

def get_last_seen_message():
    params = {'count': 1,
              'peer_id': PEER_ID}

    return json.loads(execute_in_vk(
        GET_MESSAGES_HISTORY_COMMAND,
        params
    )).get("response", {}).get("items", [])[0].get("id")

def load_new_messages():
    global last_seen_message
    params = {
        'peer_id': PEER_ID,
        'rev': 0,
        'count': LOAD_COUNT
    }

    messages = json.loads(execute_in_vk(
        GET_MESSAGES_HISTORY_COMMAND,
        params
    )).get("response", {}).get("items", [])


    messages = filter(lambda m: m["id"] > last_seen_message, messages)[::-1]

    if len(messages) > 0:
        last_seen_message = messages[-1].get("id")
        print "New last seen: ", last_seen_message
    return messages


GET_COMMAND_EXPR = re.compile("qwerty")
"""
parse command
"""
def get_command(text):
    res = GET_COMMAND_EXPR.match(text)
    if not res:
        return None
    if res.group(3):
        return res.group(1), res.group(3).strip().split(" ")
    else:
        return res.group(1), []

def log_message(message):
    return None

def log_last_messages(count=150):
    return None

#############
# operators #
#############


def ping(args, message):
    params = {'message': 'pong'}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)

def echo(args, message):
    return ping(args, message)


def hello(args, message):
    return ping(args, message)

def stat(args, message):
    return ping(args, message)

def sovet(args, message):
    return ping(args, message)

def xchange(args, message):
    return ping(args, message)

def news(args, message):
    return ping(args, message)

def russian_news(args, message):
    return ping(args, message)


NAME_TO_FUNCTOR = {
    "ping": ping,
    "echo": echo,
    "hello": hello,
    "stat": stat,
    "sovet": sovet,
    "xchange": xchange,
    "news": news,
    "russian": russian_news,
}

def commands(args, message):
    return ping(args, message)


NAME_TO_FUNCTOR["commands"] = commands

#########
# cicle #
#########


# log_last_messages()

while(True):
    if not last_seen_message:
        last_seen_message = get_last_seen_message()
        print "Selected last seen: ", last_seen_message

    messages = load_new_messages()
    for message in messages:
        command = get_command(message['body'])
        if command and command[0] in NAME_TO_FUNCTOR:
            print "Detected command", command[0], "with args:", command[1]
            NAME_TO_FUNCTOR[command[0]](command[1], message)
        else:
            print "Noncommand message: ", message['body']
            # log_message(message)

    time.sleep(1)
