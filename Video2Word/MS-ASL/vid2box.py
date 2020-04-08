from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json
import numpy as np
import cv2
import random
import shutil
from os.path import isfile, join



def convertBbox(box_norm, width, height, augment = True, fit_square= False):
    #spatial augmentation variables
    t_fac = .1 #%translation
    s_fac = .1 #%scaling
    trans_x = random.uniform(-t_fac, t_fac)
    trans_y = random.uniform(-t_fac,t_fac)
    scale_x = random.uniform(-s_fac, s_fac)
    scale_y = random.uniform(-s_fac, s_fac)

    #convert box_norm x,y
    x1 = box_norm[0]*width
    y1 = box_norm[1]*height

    #convert box_norm weight and height and scale
    box_width = box_norm[2]*width*(1-scale_x) #min 1-scale_x is .9, max is 1.1, which is 10% random scaling
    box_height = box_norm[3]*height*(1-scale_y)

    #translate box
    x1 = x1+trans_x*box_width #translate by up to +-10% of box
    y1 = y1+trans_y*box_height

    #fit square
    if fit_square:
        if box_width>=box_height:
            square_length = box_width
            y1 = y1-(square_length-box_height)/2
        if box_height>box_width:
            square_length = box_height
            x1 = x1-(square_length-box_width)/2
        x2 = x1+square_length
        y2 = y1+square_length
    else:
        x2 = x1+box_width
        y2 = y1+box_height

    return [int(x1), int(x2), int(y1), int(y2)]


def resizedAndCrop(img, box):
    #cropping

    #box may be too big now because of fit to square, so pad first
    pad_left = abs(min(box[0],0)) #adding padding if box<0
    pad_right = max(box[1]-img.shape[1],0) #x2>num_cols->pad right is x2-num_cols
    pad_top = abs(min(box[2],0))
    pad_bottom = max(box[3]-img.shape[0],0)

    # for i in range(3):
    img_padded = np.pad(img, ((pad_left, pad_right), (pad_top, pad_bottom), (0,0)), 'constant')

    #adjust box for padded image, specifically negative values
    width = box[1]-box[0]
    height = box[3]-box[2]
    x1 = max(box[0], 0)
    x2 = x1+width
    y1 = max(box[2],0)
    y2 = y1+height
    crop = img_padded[y1:y2, x1:x2]

    #resizing
    dim = (224,224)
    resized = cv2.resize(crop, dim, interpolation = cv2.INTER_AREA)
    return resized

def getImageNum(elem):
    #needed to sort images of file name images#.jpg
    return int(elem.split('.')[0][5:])


def choose64Frames(imgdir):
    #choose 64 consecutive frames randomly
    #randomly elongate first/last frame if <64 frames
    frames = (os.listdir(imgdir))
    frames.sort(key=getImageNum)
    temporal_length = 64
    if len(frames)<temporal_length:
        is_front = random.randint(0,1) #randomly decide to do front or back
        for i in range(temporal_length-len(frames)):
            if(is_front):
                ind = 0
                lab = '-'+str(i+1) #make these values negative because they're before #so no negative 0
            else:
                ind = -1
                lab = str(len(frames)+i+1) #values will be added to end #because images are 1-indexed
            source= os.path.join(imgdir,frames[ind])
            destination = os.path.join(imgdir,frames[ind].split('.')[0][0:5]+lab+'.jpg') #change image number and maintain sorting
            dest = shutil.copyfile(source, destination)
    else:
        start_index = random.randint(0,len(frames)-temporal_length)
        for i in range(len(frames)):
            if i>=start_index and i<start_index+temporal_length:
                continue
            else:
                os.unlink(os.path.join(imgdir,frames[i]))



def makeCroppedVideo(pathOut, fps, pathIn):
    frame_array = []
    files = [f for f in (os.listdir(pathIn)) if isfile(join(pathIn, f))]#for sorting the file names properly
    # files.sort(key = lambda x: x[5:-4])
    # files.sort()

    files.sort(key=getImageNum)

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

def process_video(orig_file, out_file, box, width, height):
    full_vid_path = orig_file
    box_vid_path = out_file
    box_norm = box
    w = width
    h = height
    b = convertBbox(box_norm, w, h)



    #clear temp_img_dir

    #Concerned a little bit about this part regarding the existence of the temp_dir
    temp_dir = 'temp_img/'
    for filename in os.listdir(temp_dir):
        os.unlink(os.path.join(temp_dir,filename))

    #take each frame, resize and crop it, write it to temp_dir

    cap = cv2.VideoCapture(full_vid_path)
    ind = 1

    temp_img_ext = '.jpg'
    while True:
        ret, frame = cap.read()
        if(ret):

            resized = resizedAndCrop(frame, b)
            img_str = temp_dir+'image'+str(ind)+temp_img_ext
            cv2.imwrite(img_str,resized)
            ind+=1
        else:
            break

    #sample 64 frames and then make video
    choose64Frames(temp_dir)
    makeCroppedVideo(box_vid_path, fps,temp_dir)

if __name__ == '__main__':

    #script to iterate through all of the datasets
    splits = ['train','test', 'val']
    for data_split in splits:


        with open('MSASL_'+data_split+'.json') as f:
          data = json.load(f)

        #for if things got stuck
        if(data_split=='train'):
            init_point = 0
        if(data_split=='test'):
            init_point = 0
        if(data_split=='val'):
            init_point = 0

        end_point = len(data)
        for i in range(init_point, end_point):
            #check if file was downloaded through protocol in download_umika.py
            ent = data[i]
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

            files = set(os.listdir(data_split+'_data'))
            if f_name in files:
                full_vid_path = os.path.join(data_split+'_data',f_name)
                box_vid_path = os.path.join(data_split+'_processed', f_name)
                box_norm = ent['box']
                w = ent['width']
                h = ent['height']
                b = convertBbox(box_norm, w, h)
                #open cv solution
                cap = cv2.VideoCapture(full_vid_path)
                ind = 1

                #clear temp_img_dir
                temp_dir = 'temp_img/'
                for filename in os.listdir(temp_dir):
                    os.unlink(os.path.join(temp_dir,filename))

                temp_img_ext = '.jpg'
                while True:
                    ret, frame = cap.read()
                    if(ret):

                        resized = resizedAndCrop(frame, b)
                        img_str = temp_dir+'image'+str(ind)+temp_img_ext
                        cv2.imwrite(img_str,resized)
                        ind+=1
                    else:
                        break
                choose64Frames(temp_dir)
                makeCroppedVideo(box_vid_path, fps,temp_dir)
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

                ##moviepy solution
                # with VideoFileClip(full_vid_path) as video:
                #     outvid = crop(video, x1=b[0], y1=b[1], x2=b[2], y2=b[3])
                #     outvid.write_videofile(box_vid_path, fps = fps) # default codec: 'libx264', 24 fps
