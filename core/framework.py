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

class Framework():
    def __init__(self):
        self.config = {}
        self.display = Display()
        self.colors = Colors()
        self.modulelock = RLock()
        self.coolness = {}
    def runner(self, argv):
        modules_dict, finger_dict = self.loadModules()    #eachmodule["Function"]=modules.module1.fingerprint
        self.connectTest(modules_dict, finger_dict)

    def search(self, values, searchFor):
        for k in values:
            for v in values[k]:
                if searchFor in k:
                    return v
                    return None

    def connectTest(self, modules_dict, finger_dict):
            with session() as c:
                requests.packages.urllib3.disable_warnings()
                initialConnect = c.get(self.config["HOST"], verify=False, allow_redirects=True)
                for k in finger_dict:
                    search = re.search(str(k), initialConnect.text)
                    if search:
                        print "[+] Found in " + self.search(finger_dict, str(k))
                        mod_run = self.search(finger_dict, str(k))
                        mod_import = "modules." + mod_run# + "." + mod_run
                        for test in self.coolness.keys():
                            if mod_run in test:
                                _instance = self.coolness[test]
                                _instance.payload(self.config)

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
            finger_dict = {mod_name: 'name',
                            'fingerprint': _instance.getFingerprint()}


        except Exception as e:
            # notify the user of errors
            print e
            self.display.error('Module \'%s\' disabled.' % (mod_name))
            return None
        return finger_dict

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
            self.display.error('Module \'%s\' disabled.' % (mod_name))
            return None
        return module_dict

    def loadModules(self):
        module_dict = {}
        finger_dict = {}
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

        return module_dict, finger_dict

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
        filesgroup.add_argument("-t",
            dest="threads",
            action="store",
            help="Number of threads to use for brute forcing. (not yet implemented.)")
        filesgroup.add_argument("-o",
            dest="output",
            action="store",
            help="File to output results to.")
        filesgroup.add_argument("--vhost",
            dest="vhost",
            action="store",
            help="Virtual Directory (i.e., for rapid7.com/owa enter owa). This is used for fingerprinting purposes only.")
        args = parser.parse_args()
        self.config["USERNAME"] = args.USERNAME
        self.config["PASSWORD"] = args.PASSWORD
        self.config["HOST"] = args.HOST
        self.config["domain"] = args.domain
        self.config["UserFile"] = args.UserFile
        self.config["threads"] = args.threads
        self.config["output"] = args.output
        self.config["vhost"] = args.vhost
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
    def run(self, argv):
        self.parseParameters(argv)
        if self.config["output"]:
            writer = Logger(sys.stdout, self.config["output"])
            sys.stdout = writer
        self.banner(self)
        if self.config["threads"]:
            print("This function has not been implemented yet. Threads will be set to 1...Sorry...")
        self.runner(self)
