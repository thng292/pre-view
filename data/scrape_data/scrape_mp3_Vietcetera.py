import random
import re
from time import sleep
import requests

urls = set()
srcUrls = ['https://vietcetera.com/vn/podcast/lap-rap',
'https://vietcetera.com/vn/podcast/cast-camp-2021',
'https://vietcetera.com/vn/podcast/bizff',
'https://vietcetera.com/vn/podcast/a-long-day-with-meow',
'https://vietcetera.com/vn/podcast/gen-z-truyen',
'https://vietcetera.com/vn/podcast/coi-mo',
'https://vietcetera.com/vn/podcast/nhin-thay',
'https://vietcetera.com/vn/podcast/have-a-sip',
'https://vietcetera.com/vn/podcast/dong-ra-dong-vao',
'https://vietcetera.com/vn/podcast/khang-thuong',
'https://vietcetera.com/vn/podcast/chuyen-be-xe-to',
'https://vietcetera.com/vn/podcast/vietnam-innovators',
'https://vietcetera.com/vn/podcast/mad',
'https://vietcetera.com/vn/podcast/loco',
'https://vietcetera.com/vn/podcast/noi-co-sach',
'https://vietcetera.com/vn/podcast/bit-tat-gia',
'https://vietcetera.com/vn/podcast/homecoming',
'https://vietcetera.com/vn/podcast/khong-cay-khong-ve',
'https://vietcetera.com/vn/podcast/yeu-lanh',
'https://vietcetera.com/vn/podcast/xi-ne-phi-le',
'https://vietcetera.com/vn/podcast/bit-tat-uk',
'https://vietcetera.com/vn/podcast/blueprint',
'https://vietcetera.com/vn/podcast/first-lady',
'https://vietcetera.com/vn/podcast/vietnam-innovators-tieng-viet',
'https://vietcetera.com/vn/podcast/de-men-du-ky',
'https://vietcetera.com/vn/podcast/tram-nam-san-khau',
'https://vietcetera.com/vn/podcast/backseat',
'https://vietcetera.com/vn/podcast/tom-lai-la',
'https://vietcetera.com/vn/podcast/coi-mo-happy-hour',
'https://vietcetera.com/vn/podcast/edustation',
'https://vietcetera.com/vn/podcast/tam-bit',
'https://vietcetera.com/vn/podcast/shows',
'https://vietcetera.com/vn/podcast/the-money-date',
'https://vietcetera.com/vn/podcast/ban-than-ban-than',
'https://vietcetera.com/vn/podcast/have-a-sip-after-hours',
'https://vietcetera.com/vn/podcast/duocmat',
'https://vietcetera.com/vn/podcast/bit-tat',
]

for srcUrl in srcUrls:
    response = requests.get(srcUrl,  headers={'User-agent': 'Mozilla/5.0'})
    raw = response.text
    for idx in [match.start() for match in re.finditer(".mp3", raw)]:
        startIdx = raw.rfind("http",0, idx)
        url = raw[startIdx:(idx + 4)]
        urls.add(url)
    sleep(random.random() * 2 + 1)

with open('link.txt', 'a') as file:
    for url in urls:
        file.write(url + "\n")