#!/usr/bin/env python3

import subprocess
from time import strftime, localtime
import uuid
import configparser

# function which generates pretty unique filename
def mkname():
    # localtime presented in format "%Y%m%d%M%S"
    a_part = strftime("%Y%m%d%M%S", localtime())
    # random 32-character hexadecimal string
    b_part = uuid.uuid4().hex
    name = a_part + "_" + b_part
    return name

def screenshot():
    filename = '/tmp/' + mkname() + ".png"
    subprocess.call(["import", filename])
    return filename

def configurate():
    pass

def main():
    file = screenshot()
    print(file)

if __name__ == "__main__":
    main()
