# -*- coding: utf-8 -*-

import urllib2 as url
import json
import time
import http_request_introduction as net
import re
import news_api as news_api
from HTMLParser import HTMLParser

BASE_URL = 'api.vk.com/method'
ACCESS_TOKEN = 'b6409e52ac46ca4a925793020c75c809860eecbc8356b54bb82b54d00ee2775403c5a4770c80cbdf4f18a'
# ACCESS_TOKEN = 'd2d4a44c09d78915d70db4ac9b41d480b552f46bfafc2c3bb12ddd1c0a708234f1338d917af7e2c948d30'
API_VERSION = 5.52

SEND_MESSAGE_COMMAND = 'messages.send'
GET_MESSAGES_COMMAND = 'messages.get'
GET_MESSAGES_HISTORY_COMMAND = 'messages.getHistory'
GET_USER_COMMAND = 'users.get'

USER_ID = 27396945 # 211198509 # 432392110
CHAT_ID = 78
# PEER_ID = USER_ID
PEER_ID = 2000000000 + CHAT_ID

LOAD_COUNT = 50

USER_ID_PARAM = {
    'user_id': USER_ID,
}

CHAT_ID_PARAM = {
    'chat_id': CHAT_ID,
}

DIALOG_PARAM = CHAT_ID_PARAM
# DIALOG_PARAM = USER_ID_PARAM



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


GET_COMMAND_EXPR = re.compile("^/([a-zA-Z]+)( (.*))?$")
def get_command(text):
    res = GET_COMMAND_EXPR.match(text)
    if not res:
        return None
    if res.group(3):
        return res.group(1), res.group(3).strip().split(" ")
    else:
        return res.group(1), []

def log_message(message):
    uid_to_messages[message["from_id"]] = 1 + uid_to_messages.get(message["from_id"], 0)

def log_last_messages(count=150):
    params = {'count': count,
              'rev': 0,
              'peer_id': PEER_ID}

    for message in json.loads(execute_in_vk(
            GET_MESSAGES_HISTORY_COMMAND,
            params
    )).get("response", {}).get("items", []):
        log_message(message)

#############
# operators #
#############


def ping(args, message):
    params = {'message': 'pong'}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)

def echo(args, message):
    args = message['body']
    params = {'message': " ".join(args)} if len(args) > 0 else {'message': " "}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)


def hello(args, message):
    uid = message["user_id"]
    name = json.loads(execute_in_vk(GET_USER_COMMAND, {'user_ids': uid, 'name_case': 'nom'}))["response"][0]["first_name"]

    params = {'message': 'Привет, {0}!'.format(name.encode('utf8'))}
    params.update(DIALOG_PARAM)
    execute_in_vk(SEND_MESSAGE_COMMAND, params)

    user = json.loads(execute_in_vk(GET_USER_COMMAND, {'user_ids': uid, 'name_case': 'acc'}))["response"][0]

    params['message'] = 'Приветствую {0} {1}!'.\
        format(user["first_name"].encode('utf8'), user["last_name"].encode('utf8'))
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)


def stat(args, message):
    if len(uid_to_messages.keys()) > 0:
        users = json.loads(execute_in_vk(GET_USER_COMMAND,
                                     {'user_ids': ",".join([str(i) for i in uid_to_messages.keys()]),
                                      'name_case': 'nom'}))["response"]
    else:
        users = []

    params = {
        'message': "Топ флудеров:\n" + "\n".join([
                                                     '"{0} {1}": {2} messages'.format(
                                                         user["first_name"].encode('utf8'),
                                                         user["last_name"].encode('utf8'),
                                                         uid_to_messages[user["id"]])
                                                     for user in users])
    }
    params.update(DIALOG_PARAM)

    return execute_in_vk(SEND_MESSAGE_COMMAND, params)


def sovet(args, message):
    sovet = url.urlopen("http://fucking-great-advice.ru/api/random").read()

    parser = HTMLParser()
    params = {'message': parser.unescape(json.loads(sovet)["text"]).encode('utf8')}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)

def xchange(args, message):
    if len(args) <= 0:
        args = ['USD', 'EUR']

    try:
        values = ['"{0}": {1}'.format(s,
            json.loads(url.urlopen("http://api.fixer.io/latest?base={0}&symbols=RUB".format(s)).read())["rates"]["RUB"])
              for s in args]
    except:
        values = []

    message = "\n".join(values)

    params = {'message': message}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)

def news(args, message):
    source = args[0] if len(args) > 0 else "cnn"
    print source
    params = {'message': news_api.get_news(source=source)}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)


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
    params = {'message': "Commands available:\n" + "\n".join(NAME_TO_FUNCTOR.keys())}
    params.update(DIALOG_PARAM)
    return execute_in_vk(SEND_MESSAGE_COMMAND, params)


NAME_TO_FUNCTOR["commands"] = commands

#########
# cicle #
#########


log_last_messages()

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
            log_message(message)

    time.sleep(1)
