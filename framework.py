#! /bin/python
#test 2
import argparse
from fingerprint import Fingerprint

class Framework():
    def __init__(self):
        self.config = {}
    def runner(self, argv):
        fingerprint = Fingerprint()
        fingerprint.connect(self.config)
    def parseParameters(self, argv):
        parser = argparse.ArgumentParser()
        filesgroup = parser.add_argument_group('inputs')
        filesgroup.add_argument("--host",
            dest="HOST",
            action="store",
            help="Host to test against")
        filesgroup.add_argument("-u",
            dest="USERNAME",
            action="store",
            help="Username")
        filesgroup.add_argument("-p",
            dest="PASSWORD",
            action="store",
            help="Password")
        filesgroup.add_argument("--protocol",
            dest="protocol",
            action="store",
            help="Protocol to use (i.e., http or https)")
        filesgroup.add_argument("--port",
            dest="port",
            action="store",
            help="Port to use. Default for protocol https is port 443, and http is port 80")
        filesgroup.add_argument("-U",
            dest="UserFile",
            action="store",
            help="File containing Usernames")
        args = parser.parse_args()
        self.config["USERNAME"] = args.USERNAME
        self.config["PASSWORD"] = args.PASSWORD
        self.config["HOST"] = args.HOST
        self.config["protocol"] = args.protocol
        self.config["port"] = args.port
        self.config["UserFile"] = args.UserFile
    def banner(self, argv):
        print """
            @         @          @
            @        @  @       @  @
            @       @    @    @      @
            @      @       @ @         @
            @      @                   @
            @       @                 @
                     @               @
                      @             @
                       @           @
                        @        @
                          @    @
                            @ @
                             @
                                      @@@@  @@@@  @@@@
                                      @   @ @     @
                    @@ @@   @  @      @@@@  @@@   @@@
                    @ @ @   @  @      @   @ @     @
                    @   @     @@      @@@@  @     @
                               @
                             @@@"""
        print " ---a Brute Force Framework by l0gan (@kirkphayes)"
    def run(self, argv):
        self.parseParameters(argv)
        self.banner(self)
        self.runner(self)
