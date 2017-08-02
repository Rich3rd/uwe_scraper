# uwe_scraper
A simple web scraper built to scrape subject announcements from UWE Blackboard.
Built using Python 3.
Test pages are included for demonstration and testing purposes.
Unit tests is available for 'login' method.

Current features:
- Could email announcements acquired to any email address entered.
- Command line interface to operate the program.
- Able to login using UWE credentials and select number of announcements based on subjects. 

Extensions used:
- datefinder , https://github.com/akoumjian/datefinder
- Beautiful Soup , https://www.crummy.com/software/BeautifulSoup/
- capybara-webkit , https://github.com/thoughtbot/capybara-webkit
- dryscrape , https://github.com/niklasb/dryscrape
- SSL email snippet , http://naelshiab.com/tutorial-send-email-python/
