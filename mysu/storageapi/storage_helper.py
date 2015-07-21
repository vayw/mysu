#!/usr/bin/env python3

"""
Helper functions for backend APIs
"""
import logging

def upload(path, cfg):
    #logging.basicConfig(filename=cfg['main']['log'], filemode='a', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if cfg['main']['storage'] == 'scp':
        # import scp module
        from . import scp

        res = scp.scp_put(path, cfg['scp']['host'], cfg['scp']['path'])
        logger.debug('done')

    else:
        logger.debug('not inplemented')
