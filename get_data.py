# coding=utf-8
# Author : Paul

# Get the data frame (Level 1 - Step 6)
import numpy as np
import json, os
from os import listdir
import pandas as pd
import pickle
import jieba
import jieba.analyse

print("Loading...")
with open("C:/Users/admin/Desktop/source_users_info_original.pkl",
          'rb') as i:  # get_source_user_info.py (Level 0 - Step 2)
    set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse = pickle.load(i)
print("Completed")

sid = 2482557597
str_sid = str(sid)
n_train = 33
n_test = 10

print('Loading...')
with open('C:/Users/admin/Desktop/time_' + str_sid + '.pkl', 'rb') as g:
    dict_event_time = pickle.load(g)
print('Completed')

event_part = []  # last 10 events
for event, time in list(dict_event_time.items())[-n_test:]:  # last n
    event_part.append(event)

# -------------------------
# set_all_source    (All the source uid)   [source_uid1,...]
# dict_source_user_times    (Each source user's appearance time)   {source_uid1:num1,...}
# dict_source_user_info    (Each source user's related eid)    {source_uid1:[eid1,...],...}
# list_source_user_times_reverse    (Source users' appearance rank)    [(source_uid1,num1),...]
# -------------------------
# list_source_uid = [2656274875, 1784473157, 1642512402,
#                    1618051664]  # The four source user to analyze (272,226,180,175(166)头条新闻)
#
# dict_source_user_interest = {}    (Each source user's interest list)   {source_uid1:[interest1,...],...}
# dict_eid_interest = {}    (Each event's interest list)   {eid1:[interest1,...],...}
# dict_source_user_reposters = {}   (Each source user's all reposters list)    {source_uid1:[uid1,...],...}
# list_all_event = []   (All the events to analyze)    [eid1,...]
# dict_reposter_interest = {}   (Each reposter's interest)   {uid1:[interest1,...],...}


# dict_reposters_bi_followers = {}
# dict_reposters_friends = {}
# dict_reposters_followers = {}
# dict_reposters_statuses = {}
# dict_reposters_favourites = {}
# dict_reposters_gender = {}
# dict_reposters_comments = {}
# dict_reposters_reposts = {}

# 原博主
# bi_followers_count  friends_counts  followers_count  statuses_count  favourites_count  comments_count  gender
# 转发者
# bi_followers_count  friends_counts  followers_count  statuses_count  favourites_count  comments_count  gender
# 关系
# similarity repost (0/1)


print("Loading...")
with open("C:/Users/admin/Desktop/" + str_sid + "text_analysis" + str(n_train) + ".pkl",
          'rb') as j:  # text_analysis.py (Level 2 - Step 4)
    dict_eid_interest, dict_source_user_reposters, dict_reposter_interest = pickle.load(j)
print("Completed")

print("Loading...")
with open("C:/Users/admin/Desktop/" + str_sid + "_reposters_info" + str(n_train) + ".pkl",
          'rb') as k:  # get_reposters_info.py (Level 2 - Step 5)
    dict_reposters_bi_followers, dict_reposters_friends, dict_reposters_followers, dict_reposters_statuses, dict_reposters_favourites, dict_reposters_gender, dict_reposters_comments, dict_reposters_reposts, dict_reposters_time_delta, dict_reposters_time = pickle.load(
        k)
print("Completed")


def jaccard_similarity(x, y):
    intersection_cardinality = len(set(x) & set(y))
    union_cardinality = len(set(x) | set(y))
    if union_cardinality == 0:
        return 0
    return intersection_cardinality / float(union_cardinality)


# Get the DataFrame for a specific source user's all repost info (dataset)

dict_data = {'rumor': [], 'bi_followers_count_s': [], 'friends_count_s': [], 'followers_count_s': [],
             'statuses_count_s': [], 'favourites_count_s': [], 'gender_s': [], 'comments_count_s': [],
             'repost_count_s': [], 'bi_followers_count_r': [], 'friends_count_r': [], 'followers_count_r': [],
             'statuses_count_r': [], 'favourites_count_r': [], 'gender_r': [], 'comments_count_r': [],
             'repost_count_r': [], 'similarity': [], 'time_delta': [], 'repost': []}
all_reposter = dict_source_user_reposters[sid]  # all the reposters list
all_event = event_part  # all the event to predict
i = 1
for event in all_event:  # every event
    # event_interest = dict_eid_interest[event]  # event's interest
    with open("C:/Users/admin/Desktop/weibo_info/" + event + ".pkl", 'rb') as f:
        rumor, list_sub_event, uid, time, mid, sid, source_uid = pickle.load(f)
    num = len(uid)  # number of all actions in a event
    with open("C:/Users/admin/Desktop/Weibo/" + event + ".json", encoding='utf-8') as g:
        file = g.read()
        length = len(json.loads(file))
        origin = json.loads(file)[0]  # source user post
        time_origin = origin['t']
        event_interest = jieba.analyse.extract_tags(json.loads(file)[0]['text'], topK=15, withWeight=False,
                                                    allowPOS=('n', 'nr', 'ns', 'nz', 'v'))
    for reposter in all_reposter:  # every reposter(all fans)
        dict_data['rumor'] = dict_data.get('rumor', []) + [rumor]  # rumor = 0/1
        dict_data['bi_followers_count_s'] = dict_data.get('bi_followers_count_s', []) + [origin['bi_followers_count']]
        dict_data['friends_count_s'] = dict_data.get('friends_count_s', []) + [origin['friends_count']]
        dict_data['followers_count_s'] = dict_data.get('followers_count_s', []) + [origin['followers_count']]
        dict_data['statuses_count_s'] = dict_data.get('statuses_count_s', []) + [origin['statuses_count']]
        dict_data['favourites_count_s'] = dict_data.get('favourites_count_s', []) + [origin['favourites_count']]
        dict_data['gender_s'] = dict_data.get('gender_s', []) + [origin['gender']]
        dict_data['comments_count_s'] = dict_data.get('comments_count_s', []) + [origin['comments_count']]
        dict_data['repost_count_s'] = dict_data.get('repost_count_s', []) + [origin['reposts_count']]
        if reposter in uid[1:]:  # reposted this event
            dict_data['repost'] = dict_data.get('repost', []) + [1]  # repost = 1
            index = uid.index(reposter)  # index of this user
            repost = json.loads(file)[index]  # get the repost
            times = dict_reposters_time[reposter]  # 次数
            dict_data['bi_followers_count_r'] = dict_data.get('bi_followers_count_r', []) + [
                repost['bi_followers_count']]
            dict_data['friends_count_r'] = dict_data.get('friends_count_r', []) + [repost['friends_count']]
            dict_data['followers_count_r'] = dict_data.get('followers_count_r', []) + [repost['followers_count']]
            dict_data['statuses_count_r'] = dict_data.get('statuses_count_r', []) + [repost['statuses_count']]
            dict_data['favourites_count_r'] = dict_data.get('favourites_count_r', []) + [repost['favourites_count']]
            dict_data['gender_r'] = dict_data.get('gender_r', []) + [repost['gender']]
            dict_data['comments_count_r'] = dict_data.get('comments_count_r', []) + [repost['comments_count']]
            dict_data['repost_count_r'] = dict_data.get('repost_count_r', []) + [repost['reposts_count']]
            dict_data['time_delta'] = dict_data.get('time_delta', []) + [repost['t'] - time_origin]
            dict_data['similarity'] = dict_data.get('similarity', []) + [
                jaccard_similarity(event_interest, dict_reposter_interest[reposter])]
            # update
            dict_reposter_interest[reposter] = dict_reposter_interest.get(reposter,
                                                                          []) + event_interest  # update the reposter's interest domain
            dict_reposters_bi_followers[reposter] = (times * dict_reposters_bi_followers[reposter] + repost[
                'bi_followers_count']) / (times + 1)
            dict_reposters_friends[reposter] = (times * dict_reposters_friends[reposter] + repost[
                'friends_count']) / (times + 1)
            dict_reposters_followers[reposter] = (times * dict_reposters_followers[reposter] + repost[
                'followers_count']) / (times + 1)
            dict_reposters_statuses[reposter] = (times * dict_reposters_statuses[reposter] + repost[
                'statuses_count']) / (times + 1)
            dict_reposters_favourites[reposter] = (times * dict_reposters_favourites[reposter] + repost[
                'favourites_count']) / (times + 1)
            dict_reposters_comments[reposter] = (times * dict_reposters_comments[reposter] + repost[
                'comments_count']) / (times + 1)
            dict_reposters_reposts[reposter] = (times * dict_reposters_reposts[reposter] + repost[
                'reposts_count']) / (times + 1)
            dict_reposters_time_delta[reposter] = (times * dict_reposters_time_delta[reposter] + repost[
                't'] - time_origin) / (times + 1)
            dict_reposters_time[reposter] = dict_reposters_time.get(reposter, 0) + 1
        else:  # not reposted this event
            dict_data['repost'] = dict_data.get('repost', []) + [0]  # repost = 0
            dict_data['bi_followers_count_r'] = dict_data.get('bi_followers_count_r', []) + [
                dict_reposters_bi_followers[reposter]]
            dict_data['friends_count_r'] = dict_data.get('friends_count_r', []) + [dict_reposters_friends[reposter]]
            dict_data['followers_count_r'] = dict_data.get('followers_count_r', []) + [
                dict_reposters_followers[reposter]]
            dict_data['statuses_count_r'] = dict_data.get('statuses_count_r', []) + [dict_reposters_statuses[reposter]]
            dict_data['favourites_count_r'] = dict_data.get('favourites_count_r', []) + [
                dict_reposters_favourites[reposter]]
            dict_data['gender_r'] = dict_data.get('gender_r', []) + [dict_reposters_gender[reposter]]
            dict_data['comments_count_r'] = dict_data.get('comments_count_r', []) + [dict_reposters_comments[reposter]]
            dict_data['repost_count_r'] = dict_data.get('repost_count_r', []) + [dict_reposters_reposts[reposter]]
            dict_data['time_delta'] = dict_data.get('time_delta', []) + [dict_reposters_time_delta[reposter]]
            dict_data['similarity'] = dict_data.get('similarity', []) + [
                jaccard_similarity(event_interest, dict_reposter_interest[reposter])]
    print(i, " event finished")
    i = i + 1
# print("Storing...")
# with open("C:/Users/admin/Desktop/data"+"1642088277"+".pkl",'wb') as j:
#     pickle.dump([dict_data],j)
# print("Completed")
#
# print("Loading data of "+"1642088277"+" in dict form...")
# with open("C:/Users/admin/Desktop/data"+"1642088277"+".pkl",'rb') as j:
#     dict_data=pickle.load(j)
# print("Completed")

# construct the data frame
data = pd.DataFrame({'rumor': dict_data['rumor'],
                     'bi_followers_count_s': dict_data['bi_followers_count_s'],
                     'friends_count_s': dict_data['friends_count_s'],
                     'followers_count_s': dict_data['followers_count_s'],
                     'statuses_count_s': dict_data['statuses_count_s'],
                     'favourites_count_s': dict_data['favourites_count_s'], 'gender_s': dict_data['gender_s'],
                     'comments_count_s': dict_data['comments_count_s'], 'repost_count_s': dict_data['repost_count_s'],
                     'bi_followers_count_r': dict_data['bi_followers_count_r'],
                     'friends_count_r': dict_data['friends_count_r'],
                     'followers_count_r': dict_data['followers_count_r'],
                     'statuses_count_r': dict_data['statuses_count_r'],
                     'favourites_count_r': dict_data['favourites_count_r'], 'gender_r': dict_data['gender_r'],
                     'comments_count_r': dict_data['comments_count_r'], 'repost_count_r': dict_data['repost_count_r'],
                     'similarity': dict_data['similarity'], 'time_delta': dict_data['time_delta'],
                     'repost': dict_data['repost']})
# print(data.head()) # print the head 5 lines

data.to_csv('C:/Users/admin/Desktop/data' + str_sid + '_' + str(n_train) + '-' + str(n_test) + '.csv', sep=',',
            index=False)  # save as csv

data.to_csv('C:/Users/admin/Desktop/data' + str_sid + '_' + str(n_train) + '-' + str(n_test) + '.txt', sep=',',
            index=False)  # save as txt
