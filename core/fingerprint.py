#! /usr/bin/python
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
from modules.citrixBrute2010 import citrixbrute2010

class Fingerprint():
    def connect(self, config):
        if "http" in config["protocol"]:
            with session() as c:
                requests.packages.urllib3.disable_warnings()
                if str(config["vhost"]) == 'None':
                    initialConnect = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"], verify=False)
                else:
                    initialConnect = c.get(config["protocol"] + '://' + config["HOST"] + ':' + config["port"] + "/" + config["vhost"], verify=False)
                cit = re.search('Citrix Access Gateway', initialConnect.text)
                mi = re.search('MobileIron', initialConnect.text)
                jun = re.search('dana-na', initialConnect.text)
                hpss = re.search('SiteScope', initialConnect.text)
                o365 = re.search('Office 365', initialConnect.text)
                owa = re.search('Outlook Web App', initialConnect.text)
                cit2 = re.search("Citrix/XenApp", initialConnect.text)
                if cit:
                    print "[+]  Citrix Access Gateway found. Running Citrix Brute Force Module..."
                    citrixBrute = citrixbrute()
                    citrixBrute.payload(config)
                elif cit2:
                    print "[+]  Citrix Access Gateway 2010 found. Running Citrix Brute Force Module..."
                    citrixBrute2010 = citrixbrute2010()
                    citrixBrute2010.payload(config)
                elif mi:
                    print "[+]  MobileIron found. Running MobileIron Brute Force Module..."
                    mobileiron = MobileIron()
                    mobileiron.payload(config)
                elif jun:
                    print "[+]  Juniper device found. Running Juniper Brute Force Module..."
                    juniper = JuniperBrute()
                    juniper.payload(config)
                elif hpss:
                    print "[+]  HP SiteScope found. Running SiteScope Brute Force Module..."
                    sitescope = SiteScopeBrute()
                    sitescope.payload(config)
                elif o365:
                    print "[+]  Office365 found. Running Office365 Brute Force Module..."
                    office365 = office365Brute()
                    office365.payload(config)
                elif owa:
                    print "[+]  Outlook Web App found. Running OWA Brute Force Module..."
                    owalogin = OWAlogin()
                    owalogin.payload(config)
                else:
                    print initialConnect.text
                    print "[-]  Fingerprinting Failed."
        else:
            print("Other protocols have not yet been implemented, but I'm working on it! :-)")
