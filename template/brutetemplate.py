#! /usr/bin/python
# This template will help get you started with a module
from requests import session
import requests
import re
from argparse import ArgumentParser

class ClassName():
    def somethingCool(self, config, payload):
        #Do something cool here
    def connectTest(self, config, payload):
        #Create a session and check if account is valid
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
                self.somethingCool(config, payload)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def payload(self, config):
        # Create authentication payload
        if config["UserFile"]:
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
