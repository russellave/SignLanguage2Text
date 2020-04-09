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


def load_rgb_frames_from_video(video_path, start=0, num=-1):
    vidcap = cv2.VideoCapture(video_path)
    # vidcap = cv2.VideoCapture('/home/dxli/Desktop/dm_256.mp4')

    frames = []

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, start)
    if num == -1:
        num = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    for offset in range(num):
        success, img = vidcap.read()

        w, h, c = img.shape
        sc = 224 / w
        img = cv2.resize(img, dsize=(0, 0), fx=sc, fy=sc)

        img = (img / 255.) * 2 - 1

        frames.append(img)

    return torch.Tensor(np.asarray(frames, dtype=np.float32))

def make_eval_json():
    data = {}
    d = "eval_vids" #where eval videos are

    label_map = make_label_map()
    names = os.listdir(d)
    for n in names:
        entry = {}
        entry["subset"] = "test"
        entry["action"] = [0, 1, length]
        data[n.split('.')[0]] = entry
    return data

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

    for data in dataloaders["test"]:
        inputs, labels, video_id = data  # inputs: b, c, t, h, w

        per_frame_logits = i3d(inputs)

        predictions = torch.max(per_frame_logits, dim=2)[0]
        out_labels = np.argsort(predictions.cpu().detach().numpy()[0])
        out_probs = np.sort(predictions.cpu().detach().numpy()[0])


def run_on_tensor(weights, ip_tensor, num_classes):
    i3d = InceptionI3d(400, in_channels=3)
    # i3d.load_state_dict(torch.load('models/rgb_imagenet.pt'))

    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  # nslt_2000_000700.pt nslt_1000_010800 nslt_300_005100.pt(best_results)  nslt_300_005500.pt(results_reported) nslt_2000_011400
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()

    t = ip_tensor.shape[2]
    ip_tensor.cuda()
    per_frame_logits = i3d(ip_tensor)

    predictions = F.upsample(per_frame_logits, t, mode='linear')

    predictions = predictions.transpose(2, 1)
    out_labels = np.argsort(predictions.cpu().detach().numpy()[0])

    arr = predictions.cpu().detach().numpy()[0,:,0].T

    plt.plot(range(len(arr)), F.softmax(torch.from_numpy(arr), dim=0).numpy())
    plt.show()

    return out_labels


def get_slide_windows(frames, window_size, stride=1):
    indices = torch.arange(0, frames.shape[0])
    window_indices = indices.unfold(0, window_size, stride)

    return frames[window_indices, :, :, :].transpose(1, 2)


if __name__ == '__main__':
    # ================== test i3d on a dataset ==============
    # need to add argparse
    mode = 'rgb'
    num_classes = 1041
    save_model = './checkpoints/' #doesn't matter

    root = 'eval_vids' #where data is

    train_split =  'preprocess/eval.json' #doesn't matter
    weights = 'checkpoints/nslt_1042_011260_0.456225.pt' #where weights are

    run(mode=mode, root=root, save_model=save_model, train_split=train_split, weights=weights, num_classes = num_classes)
