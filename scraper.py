#!/usr/bin/env python

from elem_wrapper import chrome_driver, ElemWrapper

import requests
from bs4 import BeautifulSoup

class Scraper(ElemWrapper):
    def __init__(self):
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chromedriver = '/Users/mhayton/github/rid-scraper/chromedriver'
        driver = chrome_driver(chrome, chromedriver)
        
        super(Scraper, self).__init__(driver)
        
        self.logger = self.logger.getChild(__name__)

    def scrape(self):
        self.driver.get('https://iub.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?storeId=39052&catalogId=10001&langId=-1')
        self.wait_until_visible('FindCourse')
        
        session = requests.Session()
        cookies = self.driver.get_cookies()
        
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        params = {
            'campusId': '31379761',
            'termId': '84429048',
            'deptId': None,
            'courseId': None,
            'sectionId': None,
            'storeId': '39052',
            'catalogId': '10001',
            'langId': '-1',
            'dropdown': 'term'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'https://iub.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?storeId=39052&catalogId=10001&langId=-1'
        }
        resp = session.post('https://iub.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd', params=params, headers=headers)
        dept_data = resp.json()

        for dept in dept_data:
            params['deptId'] = dept['categoryId']
            params['dropdown'] = 'dept'

            resp = session.post('https://iub.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd', params=params, headers=headers)
            course_data = resp.json()

            for course in course_data:
                params['courseId'] = course['categoryId']                
                params['dropdown'] = 'course'

                resp = session.post('https://iub.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd', params=params, headers=headers)
                section_data = resp.json()

                
        print resp.text
        
if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape()
