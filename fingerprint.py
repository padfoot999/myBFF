#! /bin/python
# Fingerprint Web Applications to determine which brute force module should be run.
from requests import session
import requests
import re
from citrixBrute import citrixbrute

class Fingerprint():
    def connect(self, config):
        with session() as c:
            initialConnect = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"], verify=False)
            m = re.search('Citrix', initialConnect.text)
            if m:
                print "[+]  Citrix Access Gateway found. Running Citrix Brute Force Module..."
                citrixBrute = citrixbrute()
                citrixBrute.payload(config)
            else:
                print "[-]  Not sure what the system is. I have a good idea! Create a module for it!"
