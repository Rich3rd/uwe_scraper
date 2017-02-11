from bs4 import BeautifulSoup
import urllib.request
import base64
import string
import requests

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


session = requests.post('https://blackboard.uwe.ac.uk/webapps/login/',data=payload)
#print(session.text)
print(session.cookies)
response = requests.get('https://blackboard.uwe.ac.uk/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_19_1',cookies=session.cookies)
soup = BeautifulSoup(response.text,'html.parser')
print(soup.text)
