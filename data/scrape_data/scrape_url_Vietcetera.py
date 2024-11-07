from time import sleep
from bs4 import BeautifulSoup

from selenium import webdriver
srcUrl = "https://vietcetera.com/vn/podcast"
driver = webdriver.Chrome()  
driver.get(srcUrl)  
  
# this is just to ensure that the page is loaded 
sleep(20)  
  
raw = driver.page_source 
urls = set()
soup = BeautifulSoup(raw, "html.parser")
for a in soup.find_all('a', href=True):
    if a['href'].startswith("/vn/podcast/") and  a['href'].count('/') == 3:
        urls.add("'https://vietcetera.com" + a['href'] + "',")

for url in urls:
    print(url)