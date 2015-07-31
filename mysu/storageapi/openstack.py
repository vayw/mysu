#!/usr/bin/env python3

from urllib import request
from os.path import basename

# returns tuple: auth token and management url
def swift_auth(api_host, user, key):
    req = request.Request(url=api_host)
    req.add_header('X-Auth-User', user)
    req.add_header('X-Auth-Key', key)
    token_req = request.urlopen(req)

    if token_req.status == 204:
        token = token_req.getheader('X-Auth-Token')
        management_url = token_req.getheader('X-Server-Management-Url')
    else:
        pass

    return (token, management_url)

def openstack_put(path, cfg):
    # get auth token
    token_n_url = swift_auth(cfg['openstack']['api_host'], cfg['openstack']['user'], \
                             cfg['openstack']['key'])
    with open(path, 'rb') as inf:
        img = inf.read()
    # tip container with '\'
    filename = basename(path)
    print(token_n_url[1] + "/" + cfg['openstack']['container'] + "/" + filename)
    put_request = request.Request(token_n_url[1] + "/" + cfg['openstack']['container'] \
                                    + "/" + filename, data=img, method='PUT')
    put_request.add_header('X-Auth-Token', token_n_url[0])
    put_request.add_header('Content-Type', 'image/png')
    res = request.urlopen(put_request)
