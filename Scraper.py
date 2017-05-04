# Thanks to
#
# datefinder , https://github.com/akoumjian/datefinder
# Beautiful Soup , https://www.crummy.com/software/BeautifulSoup/
# capybara-webkit , https://github.com/thoughtbot/capybara-webkit
# dryscrape , https://github.com/niklasb/dryscrape
# SSL email snippet , http://naelshiab.com/tutorial-send-email-python/
#
# Ter Jing Ng - 14033542
# UWE Computing Project
# Works for UWE Blackboard only
# 2017



from bs4 import BeautifulSoup
import dryscrape
import re
import collections
import datefinder
import getpass

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

    try:
        session.visit('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1')  # Visit the 'Courses' page
        session.wait_for(lambda: session.at_xpath('//*[@id="_186_1termCourses_noterm"]/ul'), timeout=10)
    except:
        print("Login failed")
        session = None

    return session


# Get courses names and links in Blackboard main page
def getSubjects(session):
    try:
        session.visit('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1')  # Visit the 'Courses' page
        session.wait_for(lambda: session.at_xpath('//*[@id="_186_1termCourses_noterm"]/ul'), timeout=10)
    except:
        print("Failed to obtain subjects\n")
        print("Program terminating")
        exit()

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
    try:
        session.visit(link)
        session.wait_for(lambda: session.at_xpath('//*[@id="courseMenuPalette_contents"]'))
    except:
        print("Failed to obtain subject categories")
        print("Program terminating")
        exit()

    soup = BeautifulSoup(session.body(), 'html.parser')

    for child in soup.find_all(id='courseMenuPalette_contents'):
        for child1 in child.find_all('li'):
            for child2 in child1.find_all('a'):
                subjectCategory[child2.find('span').string] = child2.attrs['href']
    return subjectCategory

# Get announcements in Subject pages
def getAnnouncements(session, link):

    subjectAnnouncements = collections.OrderedDict() # ordered dictionary

    session.visit(link)
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
def getSubjectAnnouncementsDates(session, link):

    fullAnnounceDates = [] # array to store announcement dates

    session.visit(link)
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

def getValueInDict(dict_input,input_selection):
    loopnum = 0  # reset loop count
    temp_string = ""

    for each, value in dict_input.items():
        if loopnum == input_selection:
            temp_string = value
        loopnum = loopnum + 1
    return temp_string

def compareDates(input_listOfDates, input_date):
    selectAnnouncements = 0
    datetimeTemp = datefinder.find_dates(input_date) #date from database
    for each in datetimeTemp:
        previousScrapeDate = each    #get the datetime to a variable
    for each in input_listOfDates:
        if (each >= previousScrapeDate): #new announcement
            selectAnnouncements += 1
    return selectAnnouncements

def main():
    username = str(input("Enter UWE Blackboard username: "))
    password = getpass.getpass(prompt='Enter UWE Blackboard password: ')

    print("Logging in.......")
    currentSession = login(username,password) # login and get session

    print("\n\nLogged in!")
    print ("\n\n Subject list")
    orderedDict_Subjects = getSubjects(currentSession) # get all subjects

    #print all the subjects out for user to select
    num = 0
    for each in orderedDict_Subjects:
        num = num + 1
        print([[[num]]],each)


    selection = input("\nEnter number which corresponds to subject:") #enter which subject would like to access
    #selection = 4

    # Get the subject name link
    selectedSubjectLink = getValueInDict(orderedDict_Subjects,int(selection)-1)

    orderedDict_SubjectCategory = getSubjectCategory(currentSession,appendBlackboardPrefix(selectedSubjectLink))

    num = 0
    for each in orderedDict_SubjectCategory:
        num = num + 1
        print([[[num]]],each)

    #Get the link for Announcements
    loopnum = 0
    for each , value in orderedDict_SubjectCategory.items():
        if (str(each) == "Announcements"):
            selection = loopnum
        loopnum = loopnum + 1

    print('Selected number: ' ,selection+1)
    #selection = 0 #supposed to have selection, but can only process announcements now

    # Get selected subject navigation bar link
    selectedCategoryLink = getValueInDict(orderedDict_SubjectCategory,int(selection))

    # Get all announcements
    orderedDict_announcements = getAnnouncements(currentSession,appendBlackboardPrefix(selectedCategoryLink))

    # Get announcement dates ONLY
    list_announcementDates_full = getSubjectAnnouncementsDates(currentSession,appendBlackboardPrefix(selectedCategoryLink))

    # get Dates only, and convert to DateTime
    list_announcementDates_short = processAnnounceDates(list_announcementDates_full)

    input_date = input("\nEnter a date to compare against: ")
    #input_date = '1 January 2017'

    #compare dates against entered date
    numberOfAnnouncements = compareDates(list_announcementDates_short,input_date)

    print('\nFound',numberOfAnnouncements, 'announcements' )
    listOfFinalAnnouncements = list(orderedDict_announcements.items())[:numberOfAnnouncements] #get the number of announcement entries

    #joining the list together into string
    stringOfFinalAnnouncements = '\n'.join(map(str, listOfFinalAnnouncements))

    input_email = input("\nEnter email to be sent to: ")
    #input_email = "richard_xf95@hotmail.com"

    #sending email to user
    sendEmail(str(input_email),"uwe-notify!",stringOfFinalAnnouncements)

    print('Email sent!')

if __name__ == '__main__':
    main()
