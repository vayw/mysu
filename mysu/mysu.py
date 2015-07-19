#!/usr/bin/env python3

import subprocess
from time import strftime, localtime
import uuid
import configparser
import argparse
from os import path
import sys

from storageapi import storage_helper

CONFIG = path.expanduser("~") + "/.config/mysu/mysu.conf"
TMPDIR = "/tmp/"

# function which generates pretty unique filename
def mkname():
    # localtime presented in format "%Y%m%d%M%S"
    a_part = strftime("%Y%m%d%M%S", localtime())
    # random 32-character hexadecimal string
    b_part = uuid.uuid4().hex
    name = a_part + "_" + b_part
    return name

def screenshot():
    filename = mkname() + ".png"
    subprocess.call(["import", TMPDIR + filename])
    return filename

# this function checks whether all parameters are set
def config_validator(cfg):
    storage_types = ['scp']

    if cfg['main']['storage'] not in storage_types:
        sys.exit('sorry, only this storage types supported: ', storage_types)
    if 'clipboard_option' in cfg['main']: # if option specified
        # if option value isn't in one of clipboard variants, when warn exit
        if cfg['main']['clipboard_option'] not in ['primary', 'clipboard']:
            sys.exit("clipboard_option should be 'primary or 'clipboard'")
    # check if url is set in main section
    if 'url' in cfg['main']:
        # and not empty
        if not cfg['main']['url']:
            sys.exit("'url' can't be empty")
    else:
        sys.exit("please, set 'url' option in main section of config")

    # check options for scp storage
    if cfg['main']['storage'] == 'scp':
        err = 0 # will by not 0 if we'll find configuration errors
        required_options = ['host', 'path']
        for i in required_options:
            if i in cfg['scp']: # check if required option exists
                if not cfg['scp'][i]: # check if option isn't empty
                    print(i, ' in section [scp], cannot be empty..')
                    err = err + 1
            else:
                print(i, ' in section [scp], should be set..')
                err = err + 1
        if err != 0:
            sys.exit()

# wrapper to commandline utils, at this moment we use only xclip
def copy2clipboard(buf, clipbrd='primary'):
    p = subprocess.Popen(['xclip', '-selection', clipbrd], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=buf.encode('utf-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--screenshot", action="store_true", \
                        help="capture a part of the screen and share it")
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    if path.isfile(CONFIG):
        cfg.read(CONFIG)
        config_validator(cfg)
    else:
        sys.exit("Probably config file is not valid or doesn't exists,\n\
            \rplease, create " + CONFIG)

    if args.screenshot:
        file = screenshot()
    else:
        pass

    storage_helper.upload(TMPDIR + file, cfg)
    copy2clipboard(cfg['main']['url'] + file)
    #print(file)

if __name__ == "__main__":
    main()
