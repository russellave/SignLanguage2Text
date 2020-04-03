#move all data into one place


#make json file with the dictionary: {file_name: {"subset": data_split, "action":[class #, start index, last index]}}
import os
import cv2
import json

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
        class_map[name] = index
    return class_map


def make_json():
    data = {}
    root = "../../MS-ASL"
    dirs = ["val_processed", "train_processed", "test_processed"]

    label_map = make_label_map()

    for di in dirs:
        d = os.path.join(root, di)
        names = os.listdir(d)
        for n in names:
            entry = {}
            entry["subset"] = di.split("_")[0]
            name = n.split('_')[0]
            name = name.replace('\ufb02','f')
            name = name.replace('\ufb01','fi')
            name = name.replace('#','')

            cap = cv2.VideoCapture("video.mp4")
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if name in label_map:
                label = label_map[name]
                entry["action"] = [label, 1, length]

                data[n] = entry
    with open('preprocess/msasl.json','w') as f:
        json.dump(data,f)
make_json()

#fix classes with "index class" instead of just class

def create_class_list():
    with open("label_map_asl.txt", "r") as f:
        classes = f.readlines()
        f.close()

    strip = lambda x: x.strip()

    class_strip = list(map(strip, classes))

    with open("preprocess/msasl_class_list.txt", "w") as f:
        for i in range(len(class_strip)):
            write_str = str(i) + " " + class_strip[i]+"\n"
            f.write(write_str)
