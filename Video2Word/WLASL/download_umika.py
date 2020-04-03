# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 01:00:48 2020

@author: umika
"""

import json
from pytube import YouTube
import os

with open('WLASL_v0.1.json') as f:
  data = json.load(f)

link = ['https://www.youtube.com/watch?v=WGfiiDgrq1I']
# for i in range(len(data)):
#     link.append(data[i]["url"])

#where to save
SAVE_PATH =  os.getcwd()#to_do
for i in link:
    try:
        yt = YouTube(i)
    except:
        print("Connection Error") #to handle exception


    try:
        stream = yt.streams.first()
        print(stream)
        # stream.download(SAVE_PATH)
    except:
        print("Some Error!")
print('Task Completed!')
