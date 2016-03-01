#! /bin/python
#Test framework

import sys
from framework import Framework

if __name__ == "__main__":
    framework = Framework()
    framework.run(sys.argv[1:])
