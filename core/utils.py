#! /usr/bin/python
import sys
class Display():
    def __init__(self, verbose=False, debug=False, logpath=None):
        self.VERBOSE = verbose
        self.DEBUG = debug
        self.logpath = logpath
        self.ruler = '-'

    def setLogPath(self, logpath):
        self.logpath = logpath

    def enableVerbose(self):
        self.VERBOSE = True

    def enableDebug(self):
        self.DEBUG = True

    def log(self, s, filename="processlog.txt"):
        if (self.logpath is not None):
            fullfilename = self.logpath + filename
            if not os.path.exists(os.path.dirname(fullfilename)):
                os.makedirs(os.path.dirname(fullfilename))
            fp = open(fullfilename, "a")
            if (filename == "processlog.txt"):
                fp.write(time.strftime("%Y.%m.%d-%H.%M.%S") + " - " + s + "\n")
            else:
                fp.write(s)
            fp.close()

    def _display(self, line, end="\n", flush=True, rewrite=False):
        if (rewrite):
            line = '\r' + line
        sys.stdout.write(line + end)
        if (flush):
            sys.stdout.flush()
        self.log(line)

    def error(self, line="", end="\n", flush=True, rewrite=False):
        '''Formats and presents errors.'''
        line = line[:1].upper() + line[1:]
        s = ""
        self._display(s, end=end, flush=flush, rewrite=rewrite)

    def output(self, line="", end="\n", flush=True, rewrite=False):
        '''Formats and presents normal output.'''
        s = ""
        self._display(s, end=end, flush=flush, rewrite=rewrite)

    def alert(self, line="", end="\n", flush=True, rewrite=False):
        '''Formats and presents important output.'''
        s = ""
        self._display(s, end=end, flush=flush, rewrite=rewrite)

    def verbose(self, line="", end="\n", flush=True, rewrite=False):
        '''Formats and presents output if in verbose mode.'''
        if self.VERBOSE:
            self.output("[VERBOSE] " + line, end=end, flush=True, rewrite=rewrite)

    def debug(self, line="", end="\n", flush=True, rewrite=False):
        '''Formats and presents output if in debug mode (very verbose).'''
        if self.DEBUG:
            self.output("[DEBUG]   " + line, end=end, flush=True, rewrite=rewrite)

    def yn(self, line, default=None):
        valid = {"yes": True, "y": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif (default.lower() == "yes") or (default.lower() == "y"):
            prompt = " [Y/n] "
        elif (default.lower() == "no") or (default.lower() == "n"):
            prompt = " [y/N] "
        else:
            self.alert("ERROR: Please provide a valid default value: no, n, yes, y, or None")

        while True:
            choice = self.input(line + prompt)
            if default is not None and choice == '':
                return valid[default.lower()]
            elif choice.lower() in valid:
                return valid[choice.lower()]
            else:
                self.alert("Please respond with 'yes/no' or 'y/n'.")

    def selectlist(self, line, input_list):
        answers = []

        if input_list != []:
            i = 1
            for item in input_list:
                self.output(str(i) + ": " + str(item))
                i = i + 1
        else:
            return answers

        choice = self.input(line)
        if not choice:
            return answers

        answers = (choice.replace(' ', '')).split(',')
        return answers

    def input(self, line):
        '''Formats and presents an input request to the user'''
        answer = raw_input(s)
        return answer

    def heading(self, line):
        '''Formats and presents styled header text'''
        line = Utils.to_unicode(line)
        self.output(self.ruler * len(line))
        self.output(line.upper())
        self.output(self.ruler * len(line))

    def print_list(self, title, _list):
        self.heading(title)
        if _list != []:
            for item in _list:
                self.output(item)
        else:
            self.output("None")

    def printModuleList(self, modules):
        """Print a listing of availialble modules"""
        self.output("+---------------------------+--------+--------------+-------------------------------------------------------------------------------------------+")
        self.output("| Module\t\t\t| Type   | Safety Level | Description\t\t\t\t\t\t\t\t\t\t    |")
        self.output("+---------------------------+--------+--------------+-------------------------------------------------------------------------------------------+")
        for module in modules:
            self.output("| %s | %s |      %s\t| %s"
                        %(modules[module]['name'],
                          modules[module]['type'],
                          modules[module]['safelevel'],
                          modules[module]['description']) +
                        (" " * (90 - len(modules[module]['description']))) + "|")
        self.output("+---------------------------+--------+--------------+-------------------------------------------------------------------------------------------+")

class Colors(object):
    N = '\033[m'  # native
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
