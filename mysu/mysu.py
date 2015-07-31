#!/usr/bin/env python3

import subprocess
from time import strftime, localtime
import uuid
import configparser
import argparse
from os import path, remove
import sys
import logging

from storageapi import storage_helper

CONFIG = path.expanduser("~") + "/.config/mysu/mysu.conf"
TMPDIR = "/tmp/"
DEFAULT_LOG = "/tmp/mysu.log"
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
    storage_types = ['scp', 'openstack']

    if cfg['main']['storage'] not in storage_types:
        sys.exit('sorry, only this storage types supported: ', storage_types)
    if 'clipboard' in cfg['main']: # if option specified
        # if option value isn't in one of clipboard variants, when warn exit
        if cfg['main']['clipboard'] not in ['primary', 'clipboard']:
            sys.exit("clipboard should be 'primary or 'clipboard'")
    else:
        cfg['main']['clipboard'] = 'primary'

    # check options for scp storage
    if cfg['main']['storage'] == 'scp':
        required_options = ['host', 'path', 'url']
        config_required(required_options, 'scp', cfg)

    if cfg['main']['storage'] == 'openstack':
        required_options = ['api_host', 'user', 'key', 'url']
        config_required(required_options, 'openstack', cfg)

def config_required(req, section, cfg):
    err = 0 # will be not 0 if we'll find configuration errors
    for i in req:
        if i in cfg[section]: # check if required option exists
            if not cfg[section][i]: # check if option isn't empty
                print(i, ' in section ', section, ' cannot be empty..')
                err = err + 1
        else:
            print(i, ' in section ', section, ' should be set..')
            err = err + 1
    if err != 0:
        sys.exit()

# wrapper to commandline utils, at this moment we use only xclip
def copy2clipboard(cfg, filename):
    if cfg['main']['clipboard']:
        clipbrd = cfg['main']['clipboard']
    else:
        clipbrd = 'primary'
    p = subprocess.Popen(['xclip', '-selection', clipbrd], stdin=subprocess.PIPE, close_fds=True)
    fileurl = cfg[cfg['main']['storage']]['url'] + filename
    p.communicate(input=fileurl.encode('utf-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", required=True, \
                        help="enter one of action, listed below, to perform: \
                        s - capture a part of the screen and share it")
    parser.add_argument("-d", "--debug", action="store_true", \
                        help="write debug to stdout")
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    if path.isfile(CONFIG):
        cfg.read(CONFIG)
        config_validator(cfg)
    else:
        sys.exit("Probably config file is not valid or doesn't exists,\n\
            \rplease, create " + CONFIG)

    # debug output
    # if debug key is given as argument: print to stdout (no configuration needed
    if 'log' in cfg['main']:
        if cfg['main']['log'] == 1:
            if args.debug:
                logging.basicConfig(level=logging.DEBUG)
            # if 'logfile' not specified in config OR empty: set to default
            elif 'logfile' not in cfg['main'] or not cfg['main']['logfile']:
                logging.basicConfig(filename=DEFAULT_LOG, filemode='a', level=logging.DEBUG)
                cfg['main']['logfile'] = DEFAULT_LOG
            # if 'logfile' specified in user config
            else:
                logging.basicConfig(filename=cfg['main']['logfile'], filemode='a', level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.ERROR)

    if args.action == 's':
        filename = screenshot()
    else:
        logging.info('choose one of available actions, please')
        sys.exit()

    storage_helper.upload(TMPDIR + filename, cfg)
    remove(TMPDIR + filename)
    copy2clipboard(cfg, filename)

if __name__ == "__main__":
    main()
