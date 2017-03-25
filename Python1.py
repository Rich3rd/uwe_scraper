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

courses = {}
subjectCategory = {}
subjectAnnounce = {}

fullAnnounceDates = []
announceDates = []
blackboardURL = 'https://blackboard.uwe.ac.uk'


def getCourses():
    for child in soup.find_all(id='div_186_1'):
        for child1 in child.find_all(class_='portletList-img courseListing coursefakeclass '):
            for child2 in child1.find_all('li'):
                for child3 in child2.find_all('a'):
                    courses[child3.contents] = child3.attrs['href']


def getSubjectCategory():
    for child in soup.find_all(id='courseMenuPalette_contents'):
        for child1 in child.find_all('li'):
            for child2 in child1.find_all('a'):
                subjectCategory[child2.find('span').string] = child2.attrs['href']


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
                fullAnnounceDates.append(child1.find(text = re.compile("Posted on.*?")))


def appendBlackboardPrefix(inputString):
    return blackboardURL + inputString


def processAnnounceDates():
    for each in fullAnnounceDates:
        temp = re.match("Posted on: (?P<date>.*?) o'clock .*",each)
        #print(temp.group('date'))
        temp = datefinder.find_dates(temp.group('date'))
        for each in temp:
            announceDates.append(each)


#getAnnouncements()

getSubjectAnnouncementsDates()
processAnnounceDates()

for each in announceDates:
    print(each)