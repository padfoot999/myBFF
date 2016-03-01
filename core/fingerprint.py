#! /bin/python
# Fingerprint Web Applications to determine which brute force module should be run.
from requests import session
import requests
import re
from modules.citrixBrute import citrixbrute
from modules.MobileIronBrute import MobileIron
from modules.JuniperBrute import JuniperBrute
from modules.SiteScopeBrute import SiteScopeBrute
from modules.Office365Brute import office365Brute
from modules.owaBrute import OWAlogin

class Fingerprint():
    def connect(self, config):
        with session() as c:
            initialConnect = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"], verify=False)
            m = re.search('Citrix', initialConnect.text)
            n = re.search('MobileIron', initialConnect.text)
            o = re.search('dana-na', initialConnect.text)
            p = re.search('SiteScope', initialConnect.text)
            q = re.search('Office 365', initialConnect.text)
            r = re.search('Outlook Web App', initialConnect.text)
            if m:
                print "[+]  Citrix Access Gateway found. Running Citrix Brute Force Module..."
                citrixBrute = citrixbrute()
                citrixBrute.payload(config)
            elif n:
                print "[+]  MobileIron found. Running MobileIron Brute Force Module..."
                mobileiron = MobileIron()
                mobileiron.payload(config)
            elif o:
                print "[+]  Juniper device found. Running Juniper Brute Force Module..."
                juniper = JuniperBrute()
                juniper.payload(config)
            elif p:
                print "[+]  HP SiteScope found. Running SiteScope Brute Force Module..."
                sitescope = SiteScopeBrute()
                sitescope.payload(config)
            elif q:
                print "[+]  Office365 found. Running Office365 Brute Force Module..."
                office365 = office365Brute()
                office365.payload(config)
            elif r:
                print "[+]  Outlook Web App found. Running OWA Brute Force Module..."
                owa = OWAlogin()
                owa.payload(config)
            else:
                print "[-]  Not sure what the system is. I have a good idea! Create a module for it!"
                owa = OWAlogin()
                owa.payload(config)
