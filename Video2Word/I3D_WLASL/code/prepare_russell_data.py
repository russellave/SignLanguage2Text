import os
import cv2
import json
from shutil import copyfile


#move all data into one place

def make_copy_processed_data():
    read_root = "/shared_space/asl_video"
    dirs = ["val_processed", "train_processed", "test_processed"]
    write_root = "/shared_space/asl_video/wlasl_data"
    for d in dirs:
        read = os.path.join(read_root, d)
        write = os.path.join(write_root, d)
        names = os.listdir(read)
        for n in names:
            read_file = os.path.join(read,n)
            write_file = os.path.join(write,n)
            copyfile(src, dst)


#make json file with the dictionary: {file_name: {"subset": data_split, "action":[class #, start index, last index]}}
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

            cap = cv2.VideoCapture(os.path.join(d,n))
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if name in label_map:
                label = label_map[name]
                entry["action"] = [label, 1, length]

                data[n.split('.')[0]] = entry
    with open('preprocess/msasl.json','w') as f:
        json.dump(data,f)

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

make_json()
