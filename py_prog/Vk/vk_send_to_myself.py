# -*- coding: utf-8 -*-
import vk_requests, time
import xml.etree.ElementTree as ET
import random
from collections import Counter
import re


def creat_api(vk_config, type):
    tree=ET.parse(vk_config)
    root= tree.getroot()

    data=[]

    for child in root:
        data.append(child.text)
    return vk_requests.create_api(app_id=data[0],login=data[1],password=data[2], scope=type)

api=creat_api('vkconfig.xml','messages')

id_dialogs=[ 176925457]
#id_dialogs=[49365913, 40427073, 322744157, 17208060, 59481837, 176925457, 17947600]
def get_messages(api, id_dials):
    i=0
    all_messages=[]
    for g in id_dials:
        while i!=100:
            k=api.messages.getHistory(user_id=str(g),count=200, offset=200*i, rev=1)
            i+=1
            if len(k['items'])==0:
                break
            for x in k['items']:
                for j in x.items():
                    if j[0]== 'out' and j[1]==1:
                        all_messages.append(x['body'])
            if i%3==0:
                time.sleep(2)
    return all_messages
messages=get_messages(api,id_dialogs)


def add_special_sym(messages):
    all_messages_formated=[]
    for i in messages:
        form='#'
        form+=i
        form+='&'
        all_messages_formated.append(form)
    return all_messages_formated

messages_form=add_special_sym(messages)
print(len(messages_form))



def conter(messages, n):
    full_str = ' '.join(messages)
    full_str=full_str.split(' ')
    if n==1:
        rate_1_word=Counter(full_str)
        return rate_1_word
    if n==2:
        list_2_word=[]
        rate_2_word={}
        for l,h in enumerate(full_str):
            g=''
            g+=h+' '
            if l+1!=len(full_str):
                g+=str(full_str[l+1])
                if len(re.findall('& #', g))==0:
                    list_2_word.append(g)
        for i in list_2_word:
            if i not in rate_2_word:
                rate_2_word[i]=1
            else:
                rate_2_word[i]+=1
        return rate_2_word
    if n == 3:
        list_3_word = []
        rate_3_word = {}
        for l, h in enumerate(full_str):
            g = ''
            g += h + ' '
            if l + 3 < len(full_str):
                g += str(full_str[l + 1])
                g += ' '
                g += str(full_str[l + 2])
                if len(re.findall('& #', g)) == 0:
                    list_3_word.append(g)

        for i in list_3_word:
            if i not in rate_3_word:
                rate_3_word[i] = 1
            else:
                rate_3_word[i] += 1
        return rate_3_word


rate1w=conter(messages_form,1)
rate2w=conter(messages_form,2)
rate3w=conter(messages_form,3)
print (rate2w)
print (rate3w)


def count_prob(counter_n_gr, counter_n1_gr):
    probs={}
    probs1={}
    for i in counter_n1_gr.keys():
        j=i.split(' ')
        j=j[:len(j)-1]
        j=' '.join(j)
        s = (counter_n1_gr[i])/(counter_n_gr[j])
        probs[i]=s
    for i in probs.keys():
        if len(i.split(' '))>=2:
            probs1[i]=probs[i]

    return probs1

bi_gram=count_prob(rate1w,rate2w)
tri_gram=count_prob(rate2w,rate3w)
print(bi_gram)
print (tri_gram)

def produce_sent(probs):
    final_sents = []
    g=0
    out = ''
    last_w = ''
    while g<=4:
        if len(out)==0:
            for i in probs.keys():
                rand = random.randint(0, 100) / 100
                if i[0]=='#' and probs[i]>=rand and i[-1]!='&':
                    out+=i
                    last_w=out.split(' ')[-1]
                if i[0] == '#' and probs[i] >= rand and i[-1]=='&' and i not in final_sents:
                    final_sents.append(i)
                    out=''
                    g+=1
                if len(out)>0:
                    break


        if len(out)>0:
            rand = random.randint(0, 100) / 100
            j=[]
            for i in probs.keys():
                if last_w == i.split(' ')[0] and i[0]!='#':
                    j.append(i)
            rand1=rand
            for h in j:
                if probs[h]>=rand1 and h[0]!='#':
                    out+= ' '+ h.split(' ')[-1]
                    last_w = out.split(' ')[-1]
                    if out[-1] == '&':
                        final_sents.append(out)
                        out = ''
                        g+=1
                        rand1=rand
                        break
                if probs[h]<rand:
                    rand1+=probs[h]

    return set(final_sents)

BI_DE=produce_sent(bi_gram)
TRI_DE = produce_sent(tri_gram)
print(BI_DE)
print(produce_sent(tri_gram))

def send_to_myself(api, list_mes, id_user):
    for i in list_mes:
        api.messages.send(user_id = id_user, message = i )
        print('Otpravleno')

#send_to_myself(api,BI_DE,123789558)
#send_to_myself(api,TRI_DE,123789558)
