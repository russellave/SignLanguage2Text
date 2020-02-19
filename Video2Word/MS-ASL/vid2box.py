from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json
import numpy as np
import cv2

from os.path import isfile, join


def convertBbox(box_norm, width, height):
    x1 = box_norm[0]*width
    y1 = box_norm[1]*height
    box_width = box_norm[2]*width
    box_height = box_norm[3]*height
    x2 = x1+box_width
    y2 = y1+box_height
    return [x1, y1, x2, y2]

def makeCroppedVideo(pathOut, fps):
    pathIn= 'temp_img/'
    fps = 0.5
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]#for sorting the file names properly
    # files.sort(key = lambda x: x[5:-4])
    # files.sort()
    # frame_array = []
    # files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]#for sorting the file names properly
    # files.sort(key = lambda x: x[5:-4])
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)

        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for i in range(len(frame_array)):
    # writing to a image array
        out.write(frame_array[i])
    out.release()

if __name__ == '__main__':
    splits = ['train']#,'test', 'val']
    for data_split in splits:
        files = set(os.listdir(data_split+'_data'))
        # print(files)

        with open('MSASL_'+data_split+'.json') as f:
          data = json.load(f)
        for ent in data[0:10]:
            url = ent["url"]
            gloss = ent["clean_text"]
            signer_id = ent["signer_id"]
            signer = ent["signer"]
            label = ent["label"]
            start_time = ent["start_time"]
            end_time = ent["end_time"]
            start = ent["start"]
            fps = ent["fps"]
            end = ent["end"]

            f_name = gloss+'_'+str(signer_id)+'_'+str(start)+str(end)+'.mp4'
            if f_name in files:
                full_vid_path = os.path.join(data_split+'_data',f_name)
                box_vid_path = os.path.join(data_split+'_box', f_name)
                box_norm = ent['box']
                w = ent['width']
                h = ent['height']
                b = convertBbox(box_norm, w, h)
                ##open cv solution
                # cap = cv2.VideoCapture(full_vid_path)
                # ind = 1
                # while True:
                #     ret, frame = cap.read()
                #     if(ret):
                #         cropped = frame[int(b[0]):int(b[2]), int(b[1]):int(b[3])]
                #         img_str = 'temp_img/image'+str(ind)+'.jpg'
                #         cv2.imwrite(img_str,cropped)
                #         ind+=1
                #     else:
                #         break

                ##moviepy solution
                # makeCroppedVideo(box_vid_path, fps)
                with VideoFileClip(full_vid_path) as video:
                    outvid = crop(video, x1=b[0], y1=b[1], x2=b[2], y2=b[3])
                    outvid.write_videofile(box_vid_path, fps = fps) # default codec: 'libx264', 24 fps
