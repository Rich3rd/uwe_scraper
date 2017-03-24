from bs4 import BeautifulSoup
import urllib.request
import base64
import string
import requests
import dryscrape

htmldoc = open('html text.html','r')
soup = BeautifulSoup(htmldoc,'html.parser')
#soup.find_all('a')

titles = []
urls = []

for child in soup.find_all(id='div_186_1'):
    for child1 in child.find_all(class_='portletList-img courseListing coursefakeclass '):
        for child2 in child1.find_all('li'):
            for child3 in child2.find_all('a'):
                titles.append(child3.contents)
                urls.append(child3.attrs['href'])

for each in titles:
    print(each)

for each1 in urls:
    print(each1)

#print(soup)
#print(soup.find_all('li'))