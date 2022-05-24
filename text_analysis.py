# coding=utf-8
# Author : Paul

# Text analysis of a source user's all posts (Level 1 - Step 4)
import numpy as np
import json, os
from os import listdir
import pandas as pd
import pickle
import jieba
import jieba.analyse

print("Text Analysis")

sid = 2482557597  # The source user to analyze (272,226,180,175(166)头条新闻)(>=20)(20,22,23,24)
str_sid = str(sid)
n_train = 33

print('Loading...')
with open('C:/Users/admin/Desktop/time_' + str_sid + '.pkl', 'rb') as g:  # time.py (Level 0 - Step 3)
    dict_event_time = pickle.load(g)
print('Completed')

event_part = []  # Events to proceed
for event, time in list(dict_event_time.items())[:n_train]:
    event_part.append(event)

# -----------------------------
# demo for jieba tag extraction

# import jieba
# import jieba.analyse
#
# sentence="【日媒称轻微处分拔旗事件当事人系日中共同想法】日本共同社昨日发文称，关于日本驻华大使座驾遇袭事件，中方4日对嫌疑人处以轻微处分而没有起诉是基于日中共同想法，避免走司法程序造成拖延以便尽早结束事端。文章说，日本正协调在亚太经合组织首脑会议上举行日中首脑会谈。"
# keywords = jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=('n','nr','ns','nz'))
# print(type(keywords))
# keywords2 = jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('n','nr','ns','nz'))
# print(keywords2)
# -----------------------------

# dict_source_user_interest   (Each source user's interest)   {source_uid1:[interest1,...],...}
# dict_eid_interest   (Each event's interest)   {eid1:[interest1,...],...}
# dict_source_user_reposters   (Each source user's all reposters)   {source_uid1:[uid1,...],...}
# dict_reposter_interest   (Each reposter's interest)   {uid1:[interest1,...],...}

print("Loading...")
with open("C:/Users/admin/Desktop/source_users_info_original.pkl", 'rb') as i:  # get_source_user_info.py (Level 0 -
    # Step 2)
    set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse = pickle.load(i)
print("Complete")

# set_all_source    (All the source uid)   [source_uid1,...]
# dict_source_user_times    (Each source user's appearance time)   {source_uid1:num1,...}
# dict_source_user_info    (Each source user's related eid)    {source_uid1:[eid1,...],...}
# list_source_user_times_reverse    (Source users' appearance rank)    [(source_uid1,num1),...]


print('''Get source user's interest / each eid's interest''')
# print(list_source_user_times_reverse)

# Get source users' interest & each eid's interest

# dict_source_user_interest = {}  # {uid:[interest,]}
dict_eid_interest = {}  # {eid: [interest,]}

all_eids = event_part  # A source user's all eids
for eid in all_eids:
    with open("C:/Users/admin/Desktop/Weibo/" + eid + ".json", encoding='utf-8') as g:
        file = g.read()
        length = len(json.loads(file))
        text = json.loads(file)[0]['text']
        keywords = jieba.analyse.extract_tags(text, topK=15, withWeight=False, allowPOS=('n', 'nr', 'ns', 'nz', 'v'))
        # dict_source_user_interest[sid]=dict_source_user_interest.get(sid,[])+list(keywords)
        dict_eid_interest[eid] = keywords
# print(dict_eid_interest)

print('''Get each source user's all reposters''')
# Get each source user's all reposters

dict_source_user_reposters = {}  # Each source user's reposters {source-uid:[uid1,uid2,...]}

for eid in all_eids:
    with open("C:/Users/admin/Desktop/Weibo/" + eid + ".json", 'r', encoding='utf-8') as h:
        file = h.read()
        j = json.loads(file)
        length = len(j)
        for i in range(1, length):
            reposter = j[i]['uid']  # reposter's uid
            dict_source_user_reposters[sid] = dict_source_user_reposters.get(sid, []) + [reposter]
# print(dict_source_user_reposters)

# print("Storing...")
# with open("C:/Users/admin/Desktop/source_user_temp20.pkl",'wb') as j:
#     pickle.dump([dict_source_user_interest,dict_eid_interest,dict_source_user_reposters],j)
# print("Completed")
#
# print("Loading...")
# with open("C:/Users/admin/Desktop/source_user_temp20.pkl", 'rb') as k:
#     dict_source_user_interest, dict_eid_interest, dict_source_user_reposters = pickle.load(k)
# print("Completed")

print('''Get all the reposters' interest''')
# Get all the reposters' interest(for 1 source user)

dict_reposter_interest = {}
list_all_reposter = dict_source_user_reposters[sid]  # All the reposters
for event in all_eids:  # each event
    with open("C:/Users/admin/Desktop/weibo_info/" + event + ".pkl", 'rb') as i:
        rumor, list_sub_event, uid, time, mid, sid, source_uid = pickle.load(i)
    print("Completed" + event)
    temp_event_interest = dict_eid_interest[event]
    for user in uid[1:]:  # each user(reposter)
        dict_reposter_interest[user] = dict_reposter_interest.get(user,[]) + temp_event_interest
# print(dict_reposter_interest)
for user, interest in dict_reposter_interest.items():
    dict_reposter_interest[user] = list(set(dict_reposter_interest.get(user)))

print("Storing...")
with open("C:/Users/admin/Desktop/" + str_sid + "text_analysis"+str(n_train)+".pkl", 'wb') as j:
    pickle.dump([dict_eid_interest, dict_source_user_reposters, dict_reposter_interest], j)
print("Completed")

print("Loading...")
# with open("C:/Users/admin/Desktop/"+ str_sid +"text_analysis30.pkl", 'rb') as l:
#     dict_eid_interest,dict_source_user_reposters,dict_reposter_interest=pickle.load(l)
print("Completed")

# -------------------------
# set_all_source    (All the source uid)   [source_uid1,...]
# dict_source_user_times    (Each source user's appearance time)   {source_uid1:num1,...}
# dict_source_user_info    (Each source user's related eid)    {source_uid1:[eid1,...],...}
# list_source_user_times_reverse    (Source users' appearance rank)    [(source_uid1,num1),...]
# -------------------------
# list_source_uid = [2656274875, 1784473157, 1642512402,
#                    1618051664]  # The four source user to analyze (272,226,180,175(166)头条新闻)

# dict_source_user_interest = {}    (Each source user's interest list)   {source_uid1:[interest1,...],...}
# dict_eid_interest = {}    (Each event's interest list)   {eid1:[interest1,...],...}
# dict_source_user_reposters = {}   (Each source user's all reposters list)    {source_uid1:[uid1,...],...}
# list_all_event = []   (All the events to analyze)    [eid1,...]
# dict_reposter_interest = {}   (Each reposter's interest)   {uid1:[interest1,...],...}
