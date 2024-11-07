from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

urls = set()
for i in range(1, 9):
    srcUrl = "https://www.topcv.vn/viec-lam-it?page=" + str(i)
    driver = webdriver.Chrome()  
    driver.get(srcUrl)  
    sleep(5)  
    raw = driver.page_source 
    soup = BeautifulSoup(raw, "html.parser")
    for a in soup.find_all('a', href=True):
        if a['href'].startswith("https://www.topcv.vn/viec-lam/"):
            urls.add(a['href'])

with open('link.txt', 'a') as file:
    for url in urls:
        file.write(url + "\n")