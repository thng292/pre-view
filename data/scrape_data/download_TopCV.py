import csv
import random
from time import sleep
from bs4 import BeautifulSoup
import requests

def download(srcUrl):
    print("Downloading ", srcUrl)
    response = requests.get(srcUrl,  headers={'User-agent': 'Mozilla/5.0'})
    raw = response.text
    soup = BeautifulSoup(raw, "html.parser")
    res = []
    for div in soup.find_all('div', class_="job-description__item--content"):
        res += [div.parent.findChild('h3').get_text(separator=' '), div.get_text(separator='\n')]
    resStr = ""
    title = ""
    company = soup.find('h2', class_="company-name-label").get_text(separator=' ')
    try:
        title = soup.find('h1', class_= "job-detail__info--title").get_text(separator=' ')
    except:
        title = srcUrl.replace("https://www.topcv.vn/viec-lam/", '')
        title = title[0:title.index('/')]
    for sub in res:
        p = sub.strip() + "\n"
        p = p.replace('\t', ' ')
        resStr += p
    for i in range(0, 5):
        resStr = resStr.replace("\n\n","\n")
        resStr = resStr.replace(" \n"," ")
        resStr = resStr.replace("\n "," ")
        resStr = resStr.replace("  "," ")
        title = title.replace("\t"," ")
        title = title.replace("\n\n","\n")
        title = title.replace(" \n"," ")
        title = title.replace("\n "," ")
        title = title.replace("  "," ")
    print(title)
    print(resStr)
    with open('jobData.txt', 'a') as file:
        file.write(title + "\n")
        file.write(company + "\n")
        file.write(resStr + "\n")
        file.write("\n----------------------------------\n")

with open('link.txt', 'r') as file:
    for line in file:
        download(line.strip())
        t = 5 + random.random() * 5
        sleep(t)