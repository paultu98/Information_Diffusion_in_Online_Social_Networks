# coding=utf-8
# Author : Paul

# Get all the repost events (action info) - Basic Info (Level 0 - Step 1)
# rumor   (rumor index)   0/1
# list_sub_event   (list of all sub events' eid)   [eid1,...]
# uid   (user id)   [uid1,uid2,...]
# time   (time point of action)   [time1,time2,...]
# sid   (each sub event's source mid)   [source-mid1,...]
# mid   (each sub event's message id)   [mid1,mid2,...]
# source_uid   (each sub event's source user id)   [source_uid1,...]

# Extract the repost info in each event

import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
import numpy as np
import json, os
from os import listdir
import re
import time
import datetime as dt
import pandas as pd
import seaborn as sns
import math
from collections import deque
import random
import csv
import pickle

with open("Weibo.txt") as f:
    file = f.readlines()
    for i, line in enumerate(file):
        if i >= 4533:
            eid = line.split("\t")[0].split(":")[1]  # source event id
            rumor = line.split("\t")[1].split(" ")[0].split(":")[1]  # rumor or not
            list_sub_event = line.split("\t")[2].split()  # list of all sub-event in an event
            uid = []  # user id
            time = []  # time
            sid = []  # source mid
            mid = []  # mid
            source_uid = []  # source uid
            with open("C:/Users/admin/Desktop/Weibo/" + eid + ".json", encoding='utf-8') as g:
                file = g.read()
                length = len(json.loads(file))  # number of post/repost in each event
                for i in range(0, length):
                    repost = json.loads(file)[i]  # One post / repost
                    uid.append(repost['uid'])
                    mid.append(repost['mid'])
                    time.append(repost['t'])
                    parent = repost['parent']
                    if parent is None:  # oneself's post
                        sid.append(eid)
                        source_uid.append(repost['uid'])
                    else:  # repost others' post
                        sid.append(parent)
                        source_uid.append("Others")  # need to re-check
                for j in range(0, length):
                    if source_uid[j] == "Others":
                        source_uid[j] = uid[mid.index(sid[j])]
            with open("C:/Users/admin/Desktop/weibo_info/" + eid + ".pkl", 'wb') as h:
                pickle.dump([rumor, list_sub_event, uid, time, mid, sid, source_uid], h)
            print("Completed " + eid)

# with open("C:/Users/admin/Desktop/weibo_info/" + eid + ".pkl", 'rb') as i:
#     rumor, list_sub_event, uid, time, mid, sid, source_uid = pickle.load(i)
# print("Completed" + eid)
