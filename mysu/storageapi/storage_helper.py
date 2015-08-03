#!/usr/bin/env python3

"""
Helper functions for backend APIs
"""
import logging

def upload(path, cfg):
    logger = logging.getLogger(__name__)
    if cfg['main']['storage'] == 'scp':
        # import scp module
        from . import scp

        res = scp.scp_put(path, cfg['scp']['host'], cfg['scp']['path'])
        logger.debug('done')

    elif cfg['main']['storage'] == 'openstack':
        # import openstack module
        from . import openstack

        if cfg['openstack']['typer'] == 'file':
            import subprocess
            bmime = subprocess.check_output(['file', '-b', '--mime-type', path])
            mime = bmime.decode('utf-8').strip()
        elif cfg['openstack']['typer'] == 'magic':
            import magic
            bmime = magic.from_file(path, mime=True)
            mime = bmime.decode('utf-8')
        else:
            print("unfortunately, this typer isn't implemented")
            from sys import exit
            exit()

        res = openstack.openstack_put(path, mime, cfg)
        logger.debug('done')

    else:
        logger.debug('not inplemented')
