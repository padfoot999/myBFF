#! /usr/bin/python
# Created by Kirk Hayes (l0gan)
# Part of myBFF, SMB guessing
import smb
from smb.base import SharedDevice
from smb.SMBConnection import SMBConnection
from core.nonHTTPModule import nonHTTPModule
import time


class SMBbrute(nonHTTPModule):
    def __init__(self, config, display, lock):
        super(SMBbrute, self).__init__(config, display, lock)
        self.fingerprint="SMB"
        self.response=""

    def somethingCool(self, config, userID, password, server_name, conn, connection):
            try:
                shareList = conn.listPath('C$', '//')
                print("[!]        User is an Administrator!")
            except:
                print "[-]        User is not an Administrator"

    def connectTest(self, config, userID, password, server_name, proxy):
        conn = SMBConnection(userID, password, 'pycon', server_name, use_ntlm_v2=True, domain=config["domain"], sign_options=SMBConnection.SIGN_WHEN_SUPPORTED, is_direct_tcp=True)
        connection = conn.connect(server_name, 445)
        if connection:
            print("[+]  User Credentials Successful: " + config["USERNAME"] + ":" + config["PASSWORD"])
            self.somethingCool(config, userID, password, server_name, conn, connection)
        else:
            print("[-]  Login Failed for: " + config["USERNAME"] + ":" + config["PASSWORD"])
