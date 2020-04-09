# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 01:00:48 2020

@author: umika
"""

import json
from pytube import YouTube 
import os

with open('MSASL_train.json') as f:
  data = json.load(f)

link = []
#for i in range(len(data)):
for i in range(2):
    link.append(data[i]["url"])
      
start_time = []
stop_time = []
file = []
#for i in range(len(data)):
for i in range(20):   
    start_time.append(data[i]["start_time"])
    stop_time.append(data[i]["end_time"])
    file.append(data[i]["file"])
    
#where to save 
SAVE_PATH = r"C:\Users\umika\OneDrive\Documents\Spring 2020\ECE496" #to_do 
for i in link: 
    try: 
        yt = YouTube(i) 
    except: 
        print("Connection Error") #to handle exception 
      

    try: 
        stream = yt.streams.first()
        stream.download(SAVE_PATH)
    except: 
        print("Some Error!") 
print('Task Completed!') 
        

def runBash(command):
	os.system(command)

def crop(start,end,input,output):
	string = "ffmpeg -i " + str(input) + " -ss  " + str(start) + " -to " + str(end) + " -c copy " + str(output)
	runBash(string)

#for i in range(len(data)):
for i in range(20):
    untrimmed = file[i]+".mp4"
    trimmed = file[i]+"_trim.mp4"
    crop(start_time[i],stop_time[i],untrimmed,trimmed)

