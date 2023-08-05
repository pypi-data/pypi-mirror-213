#!/usr/bin/env python
"""
stuff for network security
"""
from subprocess import call
from loguru import logger as log
from pathlib import Path
from orbit_component_base.src.orbit_shared import world


class OrbitMakeSSL:

    @property
    def crt (self):
        return (world.conf.ssl / 'ca' / 'localhost.crt').as_posix()

    @property
    def key (self):
        return (world.conf.ssl / 'ca' / 'localhost.key').as_posix()

    def open (self):
        if not Path(world.conf.make_keys):
            log.error('make_keys="{world.conf.make_keys}" cannot be found')
            return self
        world.conf.ssl.mkdir(parents=True, exist_ok=True)
        try:
            call(['sh', world.conf.make_keys, world.conf.ssl.as_posix(), world.conf.name])
        except Exception as e:
            log.exception(e)
        return self
