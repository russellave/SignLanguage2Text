import math
import os
import argparse

import matplotlib.pyplot as plt

import torch
import torch.nn as nn

from torchvision import transforms
import videotransforms

import numpy as np

import torch.nn.functional as F
from pytorch_i3d import InceptionI3d

# from nslt_dataset_all import NSLT as Dataset
from datasets.nslt_dataset_all_eval import NSLT as Dataset
import cv2



parser = argparse.ArgumentParser()
parser.add_argument('-vid_path', type=str)
parser.add_argument('-mode', type=str, help='rgb or flow')
parser.add_argument('-save_model', type=str)
parser.add_argument('-root', type=str)

args = parser.parse_args()


def video_to_tensor(pic):
    """Convert a ``numpy.ndarray`` to tensor.
    Converts a numpy.ndarray (T x H x W x C)
    to a torch.FloatTensor of shape (C x T x H x W)

    Args:
         pic (numpy.ndarray): Video to be converted to tensor.
    Returns:
         Tensor: Converted video.
    """
    return torch.from_numpy(pic.transpose([3, 0, 1, 2]))


def center_crop(img, size = 224):
    t, h, w, c = img.shape
    th, tw = (int(size), int(size))
    i = int(np.round((h - th) / 2.))
    j = int(np.round((w - tw) / 2.))
    return img[:, i:i+th, j:j+tw, :]

def load_rgb_frames_from_video(video_path, start, num):
    vidcap = cv2.VideoCapture(video_path)
    # vidcap = cv2.VideoCapture('/home/dxli/Desktop/dm_256.mp4')

    frames = []

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, start)
    for offset in range(num):
        success, img = vidcap.read()
        w, h, c = img.shape
        if w < 226 or h < 226:
            d = 226. - min(w, h)
            sc = 1 + d / min(w, h)
            img = cv2.resize(img, dsize=(0, 0), fx=sc, fy=sc)
        img = (img / 255.) * 2 - 1

        frames.append(img)

    return np.asarray(frames, dtype=np.float32)

def prepare_data_mp4(vid_path): #assume .mp4 in title
    num_frames = int(cv2.VideoCapture(vid_path).get(cv2.CAP_PROP_FRAME_COUNT))
    if mode == 'flow':
         num_frames = num_frames // 2

    label = np.zeros((num_classes, num_frames), np.float32)
    print((vid_path,0, 0, num_frames, "{}".format(vid_path)))
    vid = load_rgb_frames_from_video(vid_path, 0, num_frames)
    
    return prepare_data(vid)

def prepare_data(vid):
    imgs = video_to_tensor(center_crop(vid))
    imgs = imgs.unsqueeze(0)   
    return imgs, 0, vid_path.split('.')[0]

   
def make_label_map():
    f_name = "preprocess/msasl_class_list.txt"
    with open(f_name, "r") as f:
        classes = f.readlines()
    strip = lambda x: x.strip()
    class_strip = list(map(strip, classes))
    class_map = {}
    for c in class_strip:
        a = c.split(" ")
        index = int(a[0])
        name = a[1]
        class_map[index] = name
    return class_map

#to update model, just need to change num_classes and weights
#to update preprocessing, go to prepare_data method
def run(video,mode='rgb', weights='weights/unproc_bs4_456225.pt', num_classes = 1042):
    class_map = make_label_map()
    if type(video)==str:  
        data = prepare_data_mp4(video)
    else: 
        data = prepare_data(video)

    # setup the model
    if mode == 'flow':
        i3d = InceptionI3d(400, in_channels=2)
        i3d.load_state_dict(torch.load('weights/flow_imagenet.pt'))
    else:
        i3d = InceptionI3d(400, in_channels=3)
        i3d.load_state_dict(torch.load('weights/rgb_imagenet.pt'))
    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()
    preds = []
    inputs, labels, video_id = data
    
       
    per_frame_logits = i3d(inputs)

    predictions = torch.max(per_frame_logits, dim=2)[0]
    out_labels = np.argsort(predictions.cpu().detach().numpy()[0])
    out_probs = np.sort(predictions.cpu().detach().numpy()[0])
    print(class_map[out_labels[-1]])
    return class_map[out_labels[-1]]
    


if __name__ == '__main__':
    # ================== test i3d on a dataset ==============
    # need to add argparse
    mode = 'rgb'
    num_classes = 1042 #look at preprocess ms-asl class list

    

    weights = 'weights/unproc_bs4_456225.pt' #where weights are
    vid_path = args.vid_path

    
    #comment next two lines to try without numpy array input
    num_frames = int(cv2.VideoCapture(vid_path).get(cv2.CAP_PROP_FRAME_COUNT))
    video = load_rgb_frames_from_video(vid_path,0,num_frames)
    
    run(video,mode=mode, weights=weights, num_classes = num_classes)
