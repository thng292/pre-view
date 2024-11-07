import os
import sys
from time import sleep
import requests
import random

def download(url: str):
    file_name = os.path.basename(url)
    with open(file_name, "wb") as f:
        print("Downloading ", file_name)
        response = requests.get(url, stream=True, allow_redirects=True, headers={'User-agent': 'Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 100.0.4896.127 Safari / 537.36'})
        total_length = response.headers.get('content-length')
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
        print("\n")

with open('link.txt', 'r') as file:
    for line in file:
        download(line.strip())
        t = 5 + random.random() * 5
        sleep(t)