from bs4 import BeautifulSoup
from datetime import datetime
import datefinder
import urllib.request
import base64
import string
import requests
import dryscrape
import re
import collections
import types

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

htmldoc = open('requirement_engineering_annoucements.html','r')
soup = BeautifulSoup(htmldoc,'html.parser')

courses = {}
subjectCategory = {}
subjectAnnouncements = collections.OrderedDict()
subjectAnnouncementBody = []
selectAnnouncements = 0

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
        for child1 in child.find_all('li',class_="clearfix"):
            #print(child1.find('h3').string) #Annnouncement title
            title = child1.find('h3').string.strip(' \t\n\r')
            temp = (child1.find('span').string).strip(' \t\n\r') #Announcement time and date
            for child2 in child1.find_all(class_='vtbegenerated'):
                for child3 in child2.find_all('p'):
                    #print(temp)
                    if(type(child3.string) is not type(None)):
                        temp = temp + ((child3.string).strip(' \t\n\r')) #Announcement body
                subjectAnnouncements[title] = temp;



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

def combineStringsFromList(input):
    if (type(temp3) is list):
        temp = " "
        for each in input:
            temp = temp + str(each)
        return temp
    return

def compareDates():
    global selectAnnouncements
    datetimeTemp = datefinder.find_dates("2-1-2016") #date from database
    for each in datetimeTemp:
        previousScrapeDate = each    #get the datetime to a variable
    print(previousScrapeDate)
    for each in announceDates:
        if (each >= previousScrapeDate): #new announcement
            selectAnnouncements += 1


def sendEmail(receiverAddress,emailSubject,emailBody):
    fromaddr = "uwe.notify@gmail.com"
    toaddr = receiverAddress
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = emailSubject

    body = emailBody
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login(fromaddr, "richard95")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


getSubjectAnnouncementsDates()
processAnnounceDates()
compareDates()
getAnnouncements()
temp3 = list(subjectAnnouncements.items())[:3]

temp2 = combineStringsFromList(temp3)
print(str(temp2))

#print(list(subjectAnnouncements.items())[:3])
#sendEmail("richard_xf95@hotmail.com",)
