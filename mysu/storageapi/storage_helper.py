#!/usr/bin/env python3

"""
Helper functions for backend APIs
"""

def upload(path, cfg):
    if cfg['main']['storage'] == 'scp':
        # import scp module
        from . import scp

        res = scp.scp_put(path, cfg['scp']['host'], cfg['scp']['path'])

    else:
        print('not inplemented')
