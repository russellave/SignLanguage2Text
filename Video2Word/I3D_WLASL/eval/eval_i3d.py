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


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
parser = argparse.ArgumentParser()
parser.add_argument('-mode', type=str, help='rgb or flow')
parser.add_argument('-save_model', type=str)
parser.add_argument('-root', type=str)

args = parser.parse_args()

def make_eval_json():
    data = {}
    d = "eval_vids" #where eval videos are
    names = os.listdir(d)
    for n in names:
        entry = {}
        entry["subset"] = "test"
        cap = cv2.VideoCapture(os.path.join(d,n))
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        entry["action"] = [0, 1, length]
        data[n.split('.')[0]] = entry
    return data

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

def run(init_lr=0.1,
        max_steps=64e3,
        mode='rgb',
        root='/ssd/Charades_v1_rgb',
        train_split='charades/charades.json',
        batch_size=3 * 15,
        save_model='',
        weights=None,
        num_classes=0):
    # setup dataset
    test_transforms = transforms.Compose([videotransforms.CenterCrop(224)])

    data = make_eval_json()
    class_map = make_label_map()

    val_dataset = Dataset(train_split, 'test', root, mode, data, num_classes, test_transforms)
    val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=1,
                                                 shuffle=False, num_workers=2,
                                                 pin_memory=False)
    dataloaders = {'test': val_dataloader}
    datasets = {'test': val_dataset}

    # setup the model
    if mode == 'flow':
        i3d = InceptionI3d(400, in_channels=2)
        i3d.load_state_dict(torch.load('weights/flow_imagenet.pt'))
    else:
        i3d = InceptionI3d(400, in_channels=3)
        i3d.load_state_dict(torch.load('weights/rgb_imagenet.pt'))
    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  # nslt_2000_000700.pt nslt_1000_010800 nslt_300_005100.pt(best_results)  nslt_300_005500.pt(results_reported) nslt_2000_011400
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()
    preds = []
    for data in dataloaders["test"]:
        inputs, labels, video_id = data  # inputs: b, c, t, h, w

        per_frame_logits = i3d(inputs)

        predictions = torch.max(per_frame_logits, dim=2)[0]
        out_labels = np.argsort(predictions.cpu().detach().numpy()[0])
        out_probs = np.sort(predictions.cpu().detach().numpy()[0])
        print(class_map[out_labels[-1]])
        preds.append(class_map[out_labels[-1]])
    return preds


if __name__ == '__main__':
    # ================== test i3d on a dataset ==============
    # need to add argparse
    mode = 'rgb'
    num_classes = 1042 #look at preprocess ms-asl class list
    save_model = './checkpoints/' #doesn't matter

    root = 'eval_vids' #where data is

    train_split =  'preprocess/eval.json' #doesn't matter
    weights = 'weights/unproc_bs4_456225.pt' #where weights are

    run(mode=mode, root=root, save_model=save_model, train_split=train_split, weights=weights, num_classes = num_classes)
