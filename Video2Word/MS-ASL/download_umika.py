# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 01:00:48 2020

@author: umika, russell
"""

import json
from pytube import YouTube
import os
import traceback

from moviepy.video.io.VideoFileClip import VideoFileClip

from multiprocessing import Pool



json_dir = 'MSASL_train.json'

#save youtube video
def download_video(url, file_path, file_name, start_time, end_time, temp_path, temp_file):
    try:
        yt = YouTube(url)
        # print("Connection Error") #to handle exception
        stream = yt.streams.first()
        stream.download(temp_path, temp_file)
        # print("Some Error!")
        temp = os.path.join(temp_path, temp_file)+'.mp4'
        targ = os.path.join(file_path,file_name)+'.mp4'


        with VideoFileClip(temp) as video:
            new = video.subclip(start_time, end_time)
            new.write_videofile(targ, audio_codec='aac')
#        ffmpeg_extract_subclip(temp, start_time, end_time, targetname = targ)

    except:
        print("bad video")
        traceback.print_exc()
        f = open('bad_url.txt','a')
        f.write(url+'\n')
        f.close()

def save_bbox(data, file_path, file_name):
    name = os.path.join(file_path, file_name)+'.txt'
    f = open(name, 'w+')
    for num in data:
        f.write("%i\t" % num)
    f.close()

def process_entry(ent):
    data_split = ent["data_split"]
    url = ent["url"]
    bbox = ent["box"]
    gloss = ent["clean_text"]
    signer_id = ent["signer_id"]
    signer = ent["signer"]
    label = ent["label"]
    start_time = ent["start_time"]
    end_time = ent["end_time"]
    start = ent["start"]
    end = ent["end"]

    data_file_path = data_split+"_data"
    data_file_name = gloss+'_'+str(signer_id)+'_'+str(start)+str(end) #goal of uniqueness #str(gloss_count[gloss])
    download_video(url, data_file_path, data_file_name, start_time, end_time,'temp', 'temp_video')

    # bbox_file_path = data_split+"_bbox"
    # bbox_file_name = gloss+'_'+data_split+'_'+str(gloss_count[gloss])
    # save_bbox(bbox, bbox_file_path, bbox_file_name)




if __name__ == '__main__':
    # p = Pool(4) #num workers
    # temp_dir = 'temp' #where i'm going to put the full youtube clip (check download_video call in process_entry)

    currdir = os.getcwd()
    splits = ['test', 'val']
    for data_split in splits:
        with open('MSASL_'+data_split+'.json') as f:
          data = json.load(f)
        init_point = 0
        if(data_split=='test'):
            init_point = 3700
        for i in range(init_point, len(data)):
            ent = data[i]
            ent['data_split'] = data_split
            process_entry(ent)

            if i%100==0:
                print('===================================================')
                print('===================================================')
                print('===================================================')
                print('===================================================')
                print('===================================================')
                print('index is: '+ str(i))
                print('===================================================')
                print('===================================================')
                print('===================================================')
                print('===================================================')
                print('===================================================')



        # update_time = 100
        # init_i = 51
        # for i in range(init_i, len(data)//update_time+1):
        #     #clean and print useful information
        #     start = i*update_time
        #     end = min((i+1)*update_time, len(data))
        #     for filename in os.listdir(temp_dir):
        #         os.unlink(os.path.join(temp_dir,filename))
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #     print('starting split: '+ data_split+' start '+str(start)+' end: '+str(end))
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #     print('===================================================')
        #
        #     #run the next update_time number of samples
        #     p.map(process_entry,data[start:end])
