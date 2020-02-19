import os
import zipfile

def zipdirHelper(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zipdir(dest_file, comp_dir):
    zipf = zipfile.ZipFile(dest_file, 'w', zipfile.ZIP_DEFLATED)
    zipdirHelper(comp_dir, zipf)
    zipf.close()

def unzipdir(uncomp_dir, writeDir):

    with zipfile.ZipFile(uncomp_dir, 'r') as zipObj:
       # Extract all the contents of zip file in different directory
       zipObj.extractall(writeDir)

if __name__ == '__main__':
    # zipdir('val_data_comp.zip','val_data/')
    uncomp_file = 'val_data_comp.zip'
    unzipdir(uncomp_file)
