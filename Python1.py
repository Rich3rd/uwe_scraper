from bs4 import BeautifulSoup
from datetime import datetime
import datefinder
import urllib.request
import base64
import string
import requests
import dryscrape
import re

htmldoc = open('requirement_engineering_annoucements.html','r')
soup = BeautifulSoup(htmldoc,'html.parser')
#soup.find_all('a')

courses = {}
subjectCategory = {}
subjectAnnounce = {}
blackboardURL = 'https://blackboard.uwe.ac.uk'
matches1 = ""
matches = []
new_matches = []

def getCourses():
    for child in soup.find_all(id='div_186_1'):
        for child1 in child.find_all(class_='portletList-img courseListing coursefakeclass '):
            for child2 in child1.find_all('li'):
                for child3 in child2.find_all('a'):
                    courses[child3.contents] = child3.attrs['href']


def getSubjectCategory():
    for child7 in soup.find_all(id='courseMenuPalette_contents'):
        for child8 in child7.find_all('li'):
            for child9 in child8.find_all('a'):
                subjectCategory[child9.find('span').string] = child9.attrs['href']


def getAnnouncements():
    for child in soup.find_all(id='announcementList'):
        for child1 in child.find_all('li'):
            print(child1.find('h3').string)
            print(child1.find('span').string)
            for child2 in child1.find_all(class_='vtbegenerated'):
                for child3 in child2.find_all('p'):
                    print(child3.string)

def getSubjectAnnouncementsDates():
    for child in soup.find_all(id='announcementList'):
        for child1 in child.find_all('li'):
            if(child1.find(text = re.compile("Posted on.*?"))):
                #print(child1.find(text = re.compile("Posted on.*?")))
                matches.append(child1.find(text = re.compile("Posted on.*?")))



def appendURL(inputString):
    return blackboardURL + inputString

#getAnnouncements()

getSubjectAnnouncementsDates()

for each in matches:
    #print(each)
    print(each)
    temp_match = re.match("Posted on: (?P<date>.*?) o'clock .*",each)
    print(temp_match.group('date'))
    #new_matches.append(temp_match.group('date'))
    #print(each)

#matches1 = datefinder.find_dates(" Tuesday, 6 November 2012 15:00:54 o'clock GMT")
for each in new_matches:
    print(each)

#"Posted on: Friday, 9 November 2012 09:08:46 o'clock GMT"
#matches23 = re.match("Posted on: (?P<date>.*?) o'clock GMT","Posted on: Friday, 9 November 2012 09:08:46 o'clock GMT")
#print(matches23.group('date'))
#print(matches23.group())


