import json

def save_bbox(fwrite, data):
    f= open(fwrite,"w+")
    for num in data:
        f.write("%i\t" % num)

def download_video(url, saveto):
    s = set(url.split('.'))
    if 'youtube' in s:
        download_youtube(url,saveto+'.mp4')
    elif 'aslpro' in s:
        download_aslpro(url,saveto+'.swf')
    else:
        download_others(url,saveto+'.mp4')

#below is main

file_path = 'WLASL_v0.1.json'


with open(file_path) as ipf:
    content = json.load(ipf)

cnt_train = 0
cnt_val = 0
cnt_test = 0

for ent in content:
    gloss = ent['gloss']
    train_ind = 1
    val_ind = 1
    test_ind = 1
    for inst in ent['instances']:
        split = inst['split']

        if split == 'train':
            cnt_train += 1
            train_data_path = 'train_data/'+gloss+'_'+str(train_ind)
            download_video(inst[''])
            train_bbox_path = 'train_bbox/'+gloss+'_'+str(train_ind)
            train_ind+=1

        elif split == 'val':
            cnt_val += 1
            val_data_path = 'val_data/'+gloss+'_'+str(val_ind)
            val_bbox_path = 'val_bbox/'+gloss+'_'+str(val_ind)
            val_ind+=1

        elif split == 'test':
            cnt_test += 1
            test_data_path = 'test_data/'+gloss+'_'+str(test_ind)
            test_bbox_path = 'test_bbox/'+gloss+'_'+str(test_ind)
            test_ind +=1
        else:
            raise ValueError("Invalid split.")


print('total glosses: {}'.format(len(content)))
print('total samples: {}'.format(cnt_train + cnt_val + cnt_test))
