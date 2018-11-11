# -*- coding: utf-8 -*-

import urllib2 as url

import http_request_introduction as net

##############################
# ########### SITE ######### #
# ##### https://vk.com ##### #
##############################
# https://vk.com/dev/openapi #
##############################



###################################
#                                 #
#          Instruction:           #
# https://vk.com/apps?act=manage  #
# https://oauth.vk.com/authorize?client_id=<СЮДА>&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,notify,status,messages,wall,offline&response_type=token&v=5.65 #
#                                 #
###################################


################################
##          Methods           ##
## https://vk.com/dev/methods ##
##                            ##
################################

############################################
#                  Me:                     #
#       https://vk.com/id432264122         #
############################################



BASE_URL = 'api.vk.com/method'
ACCESS_TOKEN = '???'
API_VERSION = 5.52


def get_online_friends():
    method = 'friends.getOnline'
    address = net.construct_https_url(BASE_URL,
                            path=method,
                            params={
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
        "count": 10
    })
    # print address
    res = url.urlopen(address).read()
    print res


def get_dialogs(count = 5):
    method = 'messages.getDialogs'
    address = net.construct_https_url(BASE_URL,
                            path=method,
                            params={
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
        "count": count
    })
    # print address
    res = url.urlopen(address).read()
    print res


def read_dialog(user_id, count = 15):
    method = 'messages.getHistory'
    address = net.construct_https_url(BASE_URL,
                            path=method,
                            params={
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
        "user_id": user_id,
        "count": count,
    })
    # print address
    res = url.urlopen(address).read()
    print res


# get_online_friends()
# get_dialogs(4)
# read_dialog(432392110)




# get_dialogs

"""
{
	"response": {
		"count": 736,
		"unread_dialogs": 1,
		"items": [{
			"unread": 1,
			"message": {
				"id": 308544,
				"date": 1497007462,
				"out": 0,
				"user_id": 432392110,
				"read_state": 0,
				"title": " ... ",
				"body": "!!"
			},
			"in_read": 308543,
			"out_read": 308544
		}, {
			"message": {
				"id": 308542,
				"date": 1497003884,
				"out": 0,
				"user_id": 211198509,
				"read_state": 1,
				"title": " ... ",
				"body": "PS я б и на бургер в салюте согласился. С молочным коктейлем😻",
				"emoji": 1
			},
			"in_read": 308542,
			"out_read": 308542
		}, {
			"message": {
				"id": 308530,
				"date": 1497002501,
				"out": 0,
				"user_id": 204601720,
				"read_state": 1,
				"title": " ... ",
				"body": "",
				"attachments": [{
					"type": "photo",
					"photo": {
						"id": 456239073,
						"album_id": -3,
						"owner_id": 204601720,
						"photo_75": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b4\/xuDwpu_6g1U.jpg",
						"photo_130": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b5\/0izQNi_XFEM.jpg",
						"photo_604": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b6\/oFy9vCzeW78.jpg",
						"photo_807": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b7\/DPxKKG-5rXQ.jpg",
						"photo_1280": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b8\/a7nchWKHCFE.jpg",
						"photo_2560": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537b9\/FdR14UV-5_U.jpg",
						"width": 2080,
						"height": 1560,
						"text": "",
						"date": 1497002484,
						"access_key": "417aeb9572a9467a21"
					}
				}, {
					"type": "photo",
					"photo": {
						"id": 456239074,
						"album_id": -3,
						"owner_id": 204601720,
						"photo_75": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537be\/fLi5VzRG1Ok.jpg",
						"photo_130": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537bf\/rIt7t7Ft8F8.jpg",
						"photo_604": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c0\/0iyPE74QILU.jpg",
						"photo_807": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c1\/6OBqcieeOYA.jpg",
						"photo_1280": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c2\/5saEivvDWas.jpg",
						"photo_2560": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c3\/dq_VKUEUREg.jpg",
						"width": 2080,
						"height": 1560,
						"text": "",
						"date": 1497002493,
						"access_key": "2b06674a06f2ca7f5c"
					}
				}, {
					"type": "photo",
					"photo": {
						"id": 456239075,
						"album_id": -3,
						"owner_id": 204601720,
						"photo_75": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c8\/ITSEM1HJ70w.jpg",
						"photo_130": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537c9\/YNAFawxuKh0.jpg",
						"photo_604": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537ca\/ZqXPa_GuuLM.jpg",
						"photo_807": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537cb\/my8tfi5J8OY.jpg",
						"photo_1280": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537cc\/7IIZeXu570c.jpg",
						"photo_2560": "https:\/\/pp.userapi.com\/c637325\/v637325720\/537cd\/9EmZR2D-d4g.jpg",
						"width": 2080,
						"height": 1560,
						"text": "",
						"date": 1497002501,
						"access_key": "3642e1e1f0eb379dc8"
					}
				}]
			},
			"in_read": 308530,
			"out_read": 308530
		}, {
			"message": {
				"id": 308471,
				"date": 1496998553,
				"out": 0,
				"user_id": 6080434,
				"read_state": 1,
				"title": "Рассылка по клубу",
				"body": "Да и завтра тренировка состоится!)",
				"chat_id": 73,
				"chat_active": [336885924, 53761328, 44773005, 4324882, 11177530, 12833653, 6080434, 139592747, 1578477, 5183348, 77477457, 79894531, 183832759, 199508091, 207373751, 245791090],
				"users_count": 17,
				"admin_id": 6080434,
				"photo_50": "https:\/\/pp.userapi.com\/c626428\/v626428759\/39b8f\/NmThgS0nu_s.jpg",
				"photo_100": "https:\/\/pp.userapi.com\/c626428\/v626428759\/39b8e\/JKolOdttJsU.jpg",
				"photo_200": "https:\/\/pp.userapi.com\/c626428\/v626428759\/39b8d\/1T1ki-UQKpw.jpg"
			},
			"in_read": 308471,
			"out_read": 308471
		}]
	}
}
"""

# read_dialog

"""
{
	"response": {
		"count": 2,
		"unread": 1,
		"items": [{
			"id": 308544,
			"body": "!!",
			"user_id": 432392110,
			"from_id": 432392110,
			"date": 1497007462,
			"read_state": 0,
			"out": 0
		}, {
			"id": 308543,
			"body": "!",
			"user_id": 432392110,
			"from_id": 432392110,
			"date": 1497007017,
			"read_state": 1,
			"out": 0
		}],
		"in_read": 308543,
		"out_read": 308544
	}
}
"""