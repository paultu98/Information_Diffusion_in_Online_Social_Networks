# coding=utf-8
# Author : Paul

# Get the sequence of events for a source user according to time (Level 0 - Step 3)


import numpy as np
import json, os
from os import listdir
import pandas as pd
import math
import random
import csv
import pickle


print("Loading...")
with open("C:/Users/admin/Desktop/source_users_info_original.pkl", 'rb') as i:  # get_source_user_info.py (Level 0 -
    # Step 2)
    set_all_source, dict_source_user_times, dict_source_user_info, list_source_user_times_reverse = pickle.load(i)
print("Complete")

# Get each event's time point (事件时间排序)

sid = 2656274875
str_sid = str(sid)

events = dict_source_user_info[sid]
print(dict_source_user_info[sid])
dict_event_time = {}  # Each event's time {eid1:time1,...}

for event in events:
    with open("C:/Users/admin/Desktop/Weibo/" + event + ".json", encoding='utf-8') as f:
        file = f.read()
        dict_event_time[event] = json.loads(file)[0]['t']
dict_event_time = dict(sorted(dict_event_time.items(), key=lambda dict_event_time: dict_event_time[1]))
print(dict_event_time)

print('Storing...')
with open('C:/Users/admin/Desktop/time_' + str_sid + '.pkl', 'wb') as g:
    pickle.dump(dict_event_time,g)
print("Completed")

# print('Loading...')
# with open('C:/Users/admin/Desktop/time_' + str_sid + '.pkl', 'rb') as g:
#     dict_event_time = pickle.load(g)
# print('Completed')
