# -*- coding: utf-8 -*-

# pylint: disable=global-statement

from mongomotor import connect
from toxiccore.conf import Settings

__version__ = '0.10.0'

settings = None
dbconn = None

ENVVAR = 'TOXICSECRETS_SETTINGS'
DEFAULT_SETTINGS = 'toxicsecrets.conf'


def create_settings():
    global settings
    global dbconn

    settings = Settings(ENVVAR, DEFAULT_SETTINGS)
    dbsettings = settings.DATABASE
    dbconn = connect(**dbsettings)
