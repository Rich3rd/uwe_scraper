# Thanks to
#
# datefinder , https://github.com/akoumjian/datefinder
# Beautiful Soup , https://www.crummy.com/software/BeautifulSoup/
# capybara-webkit , https://github.com/thoughtbot/capybara-webkit
# dryscrape , https://github.com/niklasb/dryscrape
#
# Richard Ng , 2017



from bs4 import BeautifulSoup
import dryscrape
import re
import collections
import datefinder
import pprint

# email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Functions

# Login to UWE Blackboard
def login(usernameInput,passwordInput):
    session = dryscrape.Session();
    session.visit('https://blackboard.uwe.ac.uk/webapps/login/')
    name = session.at_xpath('//*[@name="user_id"]')  # Where <input name="username">
    name.set(usernameInput)
    password = session.at_xpath('//*[@name="password"]')  # Where <input name="password">
    password.set(passwordInput)
    name.form().submit() # Push the button
    return session

# Get courses names and links in Blackboard main page
def getSubjects(session):
    session.visit('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1') # Visit the 'Courses' page
    session.wait_for(lambda: session.at_xpath('//*[@id="_186_1termCourses_noterm"]/ul'))
    soup = BeautifulSoup(session.body(), 'html.parser')

    courses = collections.OrderedDict()    #Temp map to put courses and its links

    for child in soup.find_all(id='div_186_1'):
        for child1 in child.find_all(class_='portletList-img courseListing coursefakeclass '):
            for child2 in child1.find_all('li'):
                for child3 in child2.find_all('a'):
                    courses[str(child3.contents)] = child3.attrs['href']
    return courses

# Get name and link of navigation bar contents in subjects page
def getSubjectCategory(session, link):
    subjectCategory = collections.OrderedDict() #map to store subject navigation bar contents
    session.visit(link)
    session.wait_for(lambda: session.at_xpath('//*[@id="courseMenuPalette_contents"]'))
    soup = BeautifulSoup(session.body(), 'html.parser')

    for child in soup.find_all(id='courseMenuPalette_contents'):
        for child1 in child.find_all('li'):
            for child2 in child1.find_all('a'):
                subjectCategory[child2.find('span').string] = child2.attrs['href']
    return subjectCategory

# Get announcements in Subject pages
def getAnnouncements(session):
    subjectAnnouncements = collections.OrderedDict() # ordered dictionary
    soup = BeautifulSoup(session.body(), 'html.parser')

    for child in soup.find_all(id='announcementList'):
        for child1 in child.find_all('li',class_="clearfix"):
            title = child1.find('h3').string.strip(' \t\n\r')   #Announcement title
            temp = (child1.find('span').string).strip(' \t\n\r') + "  " #Announcement time and date
            for child2 in child1.find_all(class_='vtbegenerated'):
                for child3 in child2.find_all('p'):
                    if(type(child3.string) is not type(None)):
                        temp = temp + ((child3.string).strip(' \t\n\r')) #Announcement body
                subjectAnnouncements[title] = temp
    return subjectAnnouncements


# Get announcement dates ONLY
def getSubjectAnnouncementsDates(session):
    fullAnnounceDates = [] # array to store announcement dates
    soup = BeautifulSoup(session.body(), 'html.parser')
    for child in soup.find_all(id='announcementList'):
        for child1 in child.find_all('li'):
            if(child1.find(text = re.compile("Posted on.*?"))):
                fullAnnounceDates.append(child1.find(text = re.compile("Posted on.*?")))
    return fullAnnounceDates

# Further process the dates to only have date, and convert to DateTime format
def processAnnounceDates(array_FullAnnounceDates):
    announceDates = [] # array to store processed announcement dates
    for each in array_FullAnnounceDates:
        temp = re.match("Posted on: (?P<date>.*?) o'clock .*",each)
        #print(temp.group('date'))
        temp = datefinder.find_dates(temp.group('date'))
        for each in temp:
            announceDates.append(each)
    return announceDates

# Append a Blackboard prefix to a string
def appendBlackboardPrefix(inputString):
    return 'https://blackboard.uwe.ac.uk'+str(inputString).strip(' \t\n\r')

#send emails to user, from http://naelshiab.com/tutorial-send-email-python/
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

def getValueInDict(dict_input):
    loopnum = 0  # reset loop count
    temp_string = ""

    for each, value in dict_input.items():
        if loopnum == selection:
            temp_string = value
        loopnum = loopnum + 1
    return temp_string


# Get Requirements Engineering main page
#session.visit('https://blackboard.uwe.ac.uk/webapps/blackboard/execute/announcement?method=search&context=course_entry&course_id=_269718_1&handle=announcements_entry&mode=view')
#session.wait_for(lambda: session.at_xpath('//*[@id="courseMenuPalette_contents"]'))

# Get Requirement Engineering's Announcements
#session.visit('https://blackboard.uwe.ac.uk/webapps/blackboard/content/launchLink.jsp?course_id=_269718_1&tool_id=_139_1&tool_type=TOOL&mode=view&mode=reset')


currentSession = login('n2-terjing','vellapushFare19') # login and get session

orderedDict_Subjects = getSubjects(currentSession) # get all subjects

#print all the subjects out for user to select
num = 0
for each in orderedDict_Subjects:
    num = num + 1
    print([[[num]]],each)


#selection = input("enter number:") #enter which subject would like to access
selection = 4

# Get the subject name link
selectedSubjectLink = getValueInDict(orderedDict_Subjects)


orderedDict_SubjectCategory = getSubjectCategory(currentSession,appendBlackboardPrefix(selectedSubjectLink))

selection = 1 #supposed to have selection, but can only process announcements now

# Get selected subject navigation bar link
selectedCategoryLink = getValueInDict(orderedDict_SubjectCategory)

# Get announcements
orderedDict_announcements = getAnnouncements(currentSession)





