import os
import time
import urllib.request
from multiprocessing.dummy import Pool
from pytube import YouTube


def request_video(url, use_referer=False):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    referer = "" if use_referer else "http://www.aslpro.com/cgi-bin/aslpro/aslpro.cgi"
    headers = {'User-Agent': user_agent,
               'Referer': referer
               }

    request = urllib.request.Request(url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()  # The data you need

    return data


def save_video(data, saveto):
    with open(saveto, 'wb+') as f:
        f.write(data)

def download_youtube(url,saveto):
    try:
        yt = YouTube(url)
    except:
        print("Connection Error") #to handle exception


    try:
        stream = yt.streams.first()
        stream.download(saveto)
    except:
        print("Some Error!")


def download_aslpro(url, saveto):
    # url = "http://www.aslpro.com/main/b/book_english_grammar.swf"
    data = request_video(url, use_referer=True)
    # saveto = os.path.join(str('sample') + '.swf')
    save_video(data, saveto)


def download_others(url, saveto):
    # url = "https://signstock.blob.core.windows.net/signschool/videos/SignSchool%20Book.mp4"
    data = request_video(url, use_referer=False)
    # saveto = os.path.join(str('sample') + '.mp4')

    save_video(data, saveto)

import os
print(os.getcwd()+'\\'+'myvid.swf')
download_aslpro("http://www.aslpro.com/main/b/book_geography",os.getcwd()+'\\'+'myvid2.swf')
