# coding=utf-8
# Author : Paul

# Extract all the info related with source users (source user's original posts info) (Level 0 - Step 2)

import pickle
import json

# set_all_source    (All the source uid)   [source_uid1,...]
# dict_source_user_times    (Each source user's appearance time)   {source_uid1:num1,...}
# dict_source_user_info    (Each source user's related eid)    {source_uid1:[eid1,...],...}
# list_source_user_times_reverse    (Source users' appearance rank)    [(source_uid1,num1),...]

# Get all the source users' info

set_all_source = []  # all the source uid
dict_source_user_times = {}  # each source uid's appearance times
dict_source_user_info = {}  # each source uid's appearance relative eid
list_source_user_times_reverse = []  # list of each source user's appearance times (reversed order)
with open("C:/Users/admin/Desktop/Weibo.txt") as f:
    for line in f.readlines():
        eid = line.split("\t")[0].split(":")[1]  # each eid
        with open("C:/Users/admin/Desktop/Weibo/" + eid + ".json", encoding='utf-8') as g:
            file = g.read()
            source_uid = int(json.loads(file)[0]['uid'])  # get source uid
            set_all_source.append(source_uid)
            if '转发微博' not in json.loads(file)[0]['text']:  # original post
                dict_source_user_times[source_uid] = dict_source_user_times.get(source_uid, 0) + 1
            if dict_source_user_info.get(source_uid, None) is None:
                dict_source_user_info[source_uid] = eid.split(' ')
            else:
                dict_source_user_info[source_uid] = dict_source_user_info.get(source_uid) + eid.split(' ')
set_all_source = set(set_all_source)
list_source_user_times_reverse = sorted(dict_source_user_times.items(),
                                        key=lambda dict_source_user_times: dict_source_user_times[1], reverse=True)

with open("C:/Users/admin/Desktop/source_users_info_original.pkl", 'wb') as h:
    pickle.dump([set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse], h)
print("Completed")

# with open("C:/Users/admin/Desktop/source_users_info_original.pkl", 'rb') as i:
#     set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse=pickle.load(i)
# print("Completed")
