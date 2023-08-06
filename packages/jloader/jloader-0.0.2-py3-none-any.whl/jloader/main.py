import os
import re
import sys
import time
import requests
from urllib.parse import urlencode

def stdout(out):
    sys.stdout.write('\r[{}{}] {}'.format(out[0], '', ' ' * 1000))
    sys.stdout.write('\r[{}{}] {}'.format(*out))
    sys.stdout.flush()

def download(url, file):
    folder = re.search('(\./)?([0-9a-zA-Zа-яА-Я+_-]+/)+', file).group(0)
    if os.path.exists(folder) == False: os.makedirs(folder, exist_ok=True);
    
    name = re.search('[0-9a-zA-Zа-яА-Я+_-]+\.[0-9a-zA-Zа-яА-Я]+$', file).group(0)
    response = requests.get(url, stream=True)
    total = response.headers.get('content-length')

    if total is None:
        #response.content
        stdout([' ', '', f'{name} ~ url fail\n'])

        return
    if os.path.exists(file):
        local = os.path.getsize(file)

        if int(total) == local:
            stdout(['*', '', f'{name} - already\n'])

            return
        else:
            stdout([' ', '', f'{name} ~ checksum fail'])

    with open(file, 'wb') as f:
        downloaded = 0
        total = int(total)
        stdout([' ', '', ''])
        times = {}
        time_start = time.time()
        time_up = 0

        for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
            downloaded += len(data)
            f.write(data)
            done = int(13*downloaded/total)
            mb = round(downloaded/(1024*1024))
            perc = round(downloaded/total*100)
            mbs = round(downloaded/(1024*1024)/(time.time()-time_start), 1)
            sec = round((time.time()-time_start) * (total-downloaded)/downloaded)

            if (time_up+0.3) < time.time():
                stdout(['=' * done + '>', '.' * (12-done), f'{name} ~ {mb}MB {perc}% {sec}s {mbs}MB/s'])
                time_up = time.time()

        stdout(['*', '', f'{name} - done\n'])
        return

def encode(base_url, public_key):
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    return(response.json()['href'])
