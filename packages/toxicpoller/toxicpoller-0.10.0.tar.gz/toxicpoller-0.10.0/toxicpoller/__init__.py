# -*- coding: utf-8 -*-

# pylint: disable=global-statement

from toxiccore.conf import Settings

__version__ = '0.10.0'

ENVVAR = 'TOXICPOLLER_SETTINGS'
DEFAULT_SETTINGS = 'toxicpoller.conf'

settings = None


def create_settings():
    global settings

    settings = Settings(ENVVAR, DEFAULT_SETTINGS)
