import json
from random import random
import re
from time import sleep
from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
from youtube_transcript_api import YouTubeTranscriptApi

playlist = [
# AI
"https://www.youtube.com/watch?v=WbzNRTTrX0g&list=PLhQjrBD2T381PopUTYtMSstgk-hsTGkVm&index=2"
# SQL
'https://www.youtube.com/watch?v=vHYeChEf2lA&list=PLhQjrBD2T382v1MBjNOhPu9SiJ1fsD4C0&index=2',
'https://www.youtube.com/watch?v=BD08USRd2M8&list=PLhQjrBD2T382v1MBjNOhPu9SiJ1fsD4C0&index=5',
# Security
'https://www.youtube.com/watch?v=kUovJpWqEMk&list=PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE&index=2',
# OOP
'https://www.youtube.com/watch?v=e4fwY9ZsxPw&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=10',
# Regular Expressions
'https://www.youtube.com/watch?v=hy3sd9MOAcc&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=9',
# File I/O
'https://www.youtube.com/watch?v=KD-Yoel6EVQ&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=8',
# Python Libraries
'https://www.youtube.com/watch?v=MztLZWibctI&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=6',
# HTML CSS
'https://www.youtube.com/watch?v=zFZrkCIc2Oc&list=PLhQjrBD2T380xvFSUmToMMzERZ3qB5Ueu&index=2',
# SQL
'https://www.youtube.com/watch?v=YzP164YANAU&list=PLhQjrBD2T380xvFSUmToMMzERZ3qB5Ueu&index=6',
# JS
'https://www.youtube.com/watch?v=x5trGVMKTdY&list=PLhQjrBD2T380xvFSUmToMMzERZ3qB5Ueu&index=7',
# JS
'https://www.youtube.com/watch?v=X52b-8y2Hf4&list=PLhQjrBD2T382gdfveyad09Ierl_3Jh_wR&index=2',
# React
'https://www.youtube.com/watch?v=Gk6RF5k3C2M&list=PLhQjrBD2T382gdfveyad09Ierl_3Jh_wR&index=5',
# React
'https://www.youtube.com/watch?v=7O43VDOlQ_o&list=PLhQjrBD2T382gdfveyad09Ierl_3Jh_wR&index=4',
# C
'https://www.youtube.com/watch?v=a8Fyf3gwvfM&list=PLhQjrBD2T382VRUw5ZpSxQSFrxMOdFObl&index=3',
'https://www.youtube.com/watch?v=PYJYiBlto5M&list=PLhQjrBD2T382VRUw5ZpSxQSFrxMOdFObl&index=6',
# DSA
'https://www.youtube.com/watch?v=pA-8eBZvN1E&list=PLhQjrBD2T382VRUw5ZpSxQSFrxMOdFObl&index=7',
'https://www.youtube.com/watch?v=jUyQqLvg8Qw&list=PLhQjrBD2T382VRUw5ZpSxQSFrxMOdFObl&index=5',
]

for index, url in enumerate(playlist):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Progress:({index+1}/{len(playlist)})")
    print(f"Title: {yt.title}")
    audio = yt.streams.get_audio_only()
    audio.download(output_path= 'data/' ,filename= yt.video_id)
    srt = YouTubeTranscriptApi.get_transcript(yt.video_id)
    with open(f'data/{yt.video_id}.json', 'w') as f:
        json.dump(srt, f, indent=4,ensure_ascii=False)
    sleep(5 + random() * 3)

