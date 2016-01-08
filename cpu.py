# -*- coding: utf-8 -*-
"""Test beacon."""

__virtualname__ = 'cpu'

import logging

# Import Salt libs
import salt.utils

# Import Third Party Libs
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


log = logging.getLogger(__name__)


def __virtual__():
    if HAS_PSUTIL is False:
        return False
    else:
        return __virtualname__


def validate(config):
    """Validate the beacon configuration."""
    if not isinstance(config, dict):
        log.info('Configuration for cpu beacon must be a dictionary.')
        return False
    else:
        threshold = config.get('threshold', None)
        if threshold is not None:
            try:
                config['threshold'] = float(threshold)
            except ValueError:
                log.info('threshold must be a numeric value.')
                return False
    return True


def beacon(config):
    """ Report CPU% usage.

    Example Config

    .. code-block:: yaml

        beacons:
          cpu: {
            threshold: 80
          }
    """
    ret = []
    threshold = config.get('threshold', None)
    data = {"cpu%": psutil.cpu_percent()}
    if threshold is None:
        ret.append(data)
    else:
        if data["cpu%"] >= threshold:
            ret.append(data)
    return ret
