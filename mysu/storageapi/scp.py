#!/usr/bin/env python3

# simple wrapper for command line client (scp)
# NOTE: You have to set up passwordless authentication to desired host
import subprocess

def scp_put(filename, host, destination, tm_out=5):
    full_dst = host + ':' + destination
    result = subprocess.check_call(['scp', filename, full_dst], timeout=tm_out)
    return result
