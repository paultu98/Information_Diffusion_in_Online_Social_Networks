# coding=utf-8
# Author : Paul

# Get a source user's all reposters' info (Level 1 - Step 5)
import numpy as np
import json
import pandas as pd
import pickle

sid = 2482557597
str_sid = str(sid)
n_train = 33

print('Loading...')
with open('C:/Users/admin/Desktop/time_' + str_sid + '.pkl', 'rb') as g:
    dict_event_time = pickle.load(g)
print('Completed')

event_part = []  # earliest n events
for event, time in list(dict_event_time.items())[:n_train]:
    event_part.append(event)

print("Loading...")
with open("C:/Users/admin/Desktop/source_users_info_original.pkl",
          'rb') as i:  # get_source_user_info.py (Level 0 - Step 2)
    set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse = pickle.load(i)
print("Completed")

print("Loading...")
with open("C:/Users/admin/Desktop/" + str_sid + "text_analysis"+str(n_train)+".pkl",
          'rb') as l:  # text_analysis.py (Level 1 - Step 4)
    dict_eid_interest, dict_source_user_reposters, dict_reposter_interest = pickle.load(l)
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


# dict_reposters_bi_followers[reposter] = dict_reposters_bi_followers.get(reposter, []) + [repost['bi_followers_count']]
# dict_reposters_friends[reposter] = dict_reposters_bi_followers.get(reposter, []) + [repost['friends_count']]
# dict_reposters_followers[reposter] = dict_reposters_followers.get(reposter, []) + [repost['followers_count']]
# dict_reposters_statuses[reposter] = dict_reposters_statuses.get(reposter, []) + [repost['statuses_count']]
# dict_reposters_favourites[reposter] = dict_reposters_favourites.get(reposter, []) + [repost['favourites_count']]
# dict_reposters_gender[reposter] = repost['gender']
# dict_reposters_comments[reposter] = dict_reposters_comments.get(reposter, []) + [repost['comments_count']]
# dict_reposters_reposts[reposter] = dict_reposters_reposts.get(reposter, []) + [repost['reposts_count']]


dict_reposters_bi_followers = {}
dict_reposters_friends = {}
dict_reposters_followers = {}
dict_reposters_statuses = {}
dict_reposters_favourites = {}
dict_reposters_gender = {}

dict_reposters_comments = {}
dict_reposters_reposts = {}
dict_reposters_time_delta = {}
dict_reposters_time = {}  # times

all_reposter = dict_source_user_reposters[sid]  # all the reposters list
all_event = event_part  # all the events
for event in all_event:
    with open("C:/Users/admin/Desktop/Weibo/" + event + ".json", encoding='utf-8') as g:
        file = g.read()
        length = len(json.loads(file))  # number of post/repost in each event
        t = json.loads(file)[0]['t']
        for i in range(1, length):
            repost = json.loads(file)[i]
            reposter = repost['uid']
            dict_reposters_bi_followers[reposter] = dict_reposters_bi_followers.get(reposter, []) + [
                repost['bi_followers_count']]
            dict_reposters_friends[reposter] = dict_reposters_bi_followers.get(reposter, []) + [repost['friends_count']]
            dict_reposters_followers[reposter] = dict_reposters_followers.get(reposter, []) + [
                repost['followers_count']]
            dict_reposters_statuses[reposter] = dict_reposters_statuses.get(reposter, []) + [repost['statuses_count']]
            dict_reposters_favourites[reposter] = dict_reposters_favourites.get(reposter, []) + [
                repost['favourites_count']]
            dict_reposters_gender[reposter] = repost['gender']
            dict_reposters_comments[reposter] = dict_reposters_comments.get(reposter, []) + [repost['comments_count']]
            dict_reposters_reposts[reposter] = dict_reposters_reposts.get(reposter, []) + [repost['reposts_count']]
            dict_reposters_time_delta[reposter] = dict_reposters_time_delta.get(reposter, []) + [repost['t'] - t]
            dict_reposters_time[reposter] = dict_reposters_time.get(reposter,0)+1
    print("Completed" + event)
print("Taking average...")
for key, value in dict_reposters_bi_followers.items():
    dict_reposters_bi_followers[key] = np.mean(value)
for key, value in dict_reposters_friends.items():
    dict_reposters_friends[key] = np.mean(value)
for key, value in dict_reposters_followers.items():
    dict_reposters_followers[key] = np.mean(value)
for key, value in dict_reposters_statuses.items():
    dict_reposters_statuses[key] = np.mean(value)
for key, value in dict_reposters_favourites.items():
    dict_reposters_favourites[key] = np.mean(value)
for key, value in dict_reposters_comments.items():
    dict_reposters_comments[key] = np.mean(value)
for key, value in dict_reposters_reposts.items():
    dict_reposters_reposts[key] = np.mean(value)
for key, value in dict_reposters_time_delta.items():
    dict_reposters_time_delta[key] = np.mean(value)
print("Storing...")
with open("C:/Users/admin/Desktop/" + str_sid + "_reposters_info"+str(n_train)+".pkl", 'wb') as k:
    pickle.dump([dict_reposters_bi_followers, dict_reposters_friends, dict_reposters_followers, dict_reposters_statuses,
                 dict_reposters_favourites, dict_reposters_gender, dict_reposters_comments, dict_reposters_reposts,
                 dict_reposters_time_delta,dict_reposters_time], k)
print("Completed")

# print("Loading...") with open("C:/Users/admin/Desktop/" + str_sid + "_reposters_info.pkl", 'rb') as k:
# dict_reposters_bi_followers, dict_reposters_friends, dict_reposters_followers, dict_reposters_statuses,
# dict_reposters_favourites, dict_reposters_gender, dict_reposters_comments, dict_reposters_reposts,
# dict_reposters_time_delta=pickle.load(k) print("Completed")
