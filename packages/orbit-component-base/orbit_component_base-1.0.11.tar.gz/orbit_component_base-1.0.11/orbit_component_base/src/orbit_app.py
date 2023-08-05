#!/usr/bin/env python3
from aiohttp import web
from aiohttp.web_runner import GracefulExit
from argparse import ArgumentParser
from asyncio import sleep
from loguru import logger as log
from multiprocessing import freeze_support, set_start_method
from socketio import AsyncServer
from ssl import create_default_context, Purpose
from sys import argv, exit
#
# These can be overridden
#
from orbit_component_base.src.orbit_router import OrbitRouter
from orbit_component_base.src.orbit_config import OrbitConfig
from orbit_component_base.src.orbit_database import OrbitDatabase
from orbit_component_base.src.orbit_logger import OrbitLogger
from orbit_component_base.src.orbit_make_ssl import OrbitMakeSSL
#
# These you really don't want to override
#
from orbit_component_base.src.orbit_plugins import Plugins
from orbit_component_base.src.orbit_shared import world


class OrbitMainBase:

    APPLICATION = 'orbit_demo'
    PLUGIN_FOLDER = 'orbit_plugins'
    ROUTER = OrbitRouter
    CONFIG = OrbitConfig
    MAINDB = OrbitDatabase
    LOGGER = OrbitLogger
    MAKSSL = OrbitMakeSSL
    SERVER_PARAMS = {
        'async_mode': 'aiohttp',
        'async_handlers': True,
        'engineio_logger': False,
        'cors_allowed_origins': '*'
    }

    def __init__ (self, app=None):
        if app:
            self.APPLICATION = app
        self._router = None

    async def startup (self, app=None):
        if world.conf.sio_debug:
            self.SERVER_PARAMS['logger'] = self.LOGGER()
        sio = world.sio = AsyncServer(**self.SERVER_PARAMS)
        odb = self.MAINDB().open()
        
        for plugin in Plugins('Plugin'):
            plugin = plugin.Plugin(odb=odb).open().register(sio)
            sio.attach(app, socketio_path=plugin.ns)
            self._router.add_namespace(plugin.NAMESPACE)

    async def shutdown(self, app=None):
        await sleep(1)
        raise GracefulExit()

    def run (self):
        set_start_method('spawn')
        freeze_support()
       
        world.conf = self.CONFIG(self.APPLICATION).open()       

        parser = ArgumentParser()
        for plugin in Plugins('Args'):
            plugin.Args(parser=parser).setup()
        world.args = parser.parse_args()        

        if not world.args.run:
            odb = self.MAINDB().open()
            for plugin in Plugins('Plugin'):
                plugin = plugin.Plugin(odb=odb).open(nql=False)
            for plugin in Plugins('Args'):
                plugin.Args(parser=parser).open(odb, world.args).process()
            print('Please add "run" if you wish to launch the application')
            exit()
  
        self._router = router = self.ROUTER()
        app = router.application()
        app.on_startup.append(self.startup)
        app.on_shutdown.append(self.shutdown)
        try:
            if world.conf.secure:
                ssl = self.MAKSSL().open()        
                ssl_context = create_default_context(Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(ssl.crt, ssl.key)
                web.run_app(
                    app,
                    handle_signals=False,
                    host=world.conf.host,
                    port=world.conf.port,
                    ssl_context=ssl_context)            
            else:
                web.run_app(
                    app,
                    host=world.conf.host,
                    port=world.conf.port)                   
        except Exception as e:
            log.exception(e)
        finally:
            print()
            log.info('Shutdown')
            raise GracefulExit()
