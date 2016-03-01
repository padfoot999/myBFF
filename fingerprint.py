#! /bin/python
# Fingerprint Web Applications to determine which brute force module should be run.
from requests import session
import requests
import re
from citrixBrute import citrixbrute
from MobileIronBrute import MobileIron

class Fingerprint():
    def connect(self, config):
        with session() as c:
            initialConnect = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"], verify=False)
            #print initialConnect.text
            m = re.search('Citrix', initialConnect.text)
            n = re.search('MobileIron', initialConnect.text)
            if m:
                print "[+]  Citrix Access Gateway found. Running Citrix Brute Force Module..."
                citrixBrute = citrixbrute()
                citrixBrute.payload(config)
            elif n:
                print "[+]  MobileIron found. Running MobileIron Brute Force Module..."
                mobileiron = MobileIron()
                mobileiron.payload(config)
            else:
                print "[-]  Not sure what the system is. I have a good idea! Create a module for it!"
