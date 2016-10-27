


class nonHTTPModule(object):
    def __init__(self, config, display, lock):
        self.fingerprint = ""
        self.name = ""
        self.description = ""
        self.type = ""
        self.response = ""
        self.protocol = ""

    def getFingerprint(self):
        return self.fingerprint

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getType(self):
        return self.type

    def getResponse(self):
        return self.response

    def doSomethingCool(self):
        return

    def getProtocol(self):
        return self.protocol
