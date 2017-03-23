from bs4 import BeautifulSoup
import urllib.request
import base64
import string
import requests
import dryscrape

class BlackboardSession():
    def __init__(self, user, password):
        self.session = requests.session()
        self.password = base64.b64encode('vellapushFare19')
        self.username = 'n2-terjing'
        self.payload = {
            'login': 'Login',
            'action': 'login',
            'user_id': self.username,
            'encoded_pw': self.password,
            }
        self.url = 'https://blackboard.uwe.ac.uk'
        self.session.post(self.url, data=self.payload)

payload = {
            'login': 'Login',
            'action': 'login',
            'user_id': 'n2-terjing',
            'password': 'vellapushFare19',
            }


#session = requests.post('https://blackboard.uwe.ac.uk/webapps/login/',data=payload)

session = dryscrape.Session();
session.visit('https://blackboard.uwe.ac.uk/webapps/login/')
name = session.at_xpath('//*[@name="user_id"]') # Where <input name="username">
name.set('n2-terjing')
password = session.at_xpath('//*[@name="password"]') # Where <input name="password">
password.set('vellapushFare19')
# Push the button
name.form().submit()
session.visit('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1')
#print(session.text)
#print(session.cookies)
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#response = requests.get('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_19_1',cookies=session.cookies,headers=headers)
#response = requests.get('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1',cookies=session.cookies)
session.wait_for(lambda: session.at_xpath('//*[@id="_186_1termCourses_noterm"]/ul'))

#Added comment for testing
soup = BeautifulSoup(session.body(),'html.parser')
print(soup)