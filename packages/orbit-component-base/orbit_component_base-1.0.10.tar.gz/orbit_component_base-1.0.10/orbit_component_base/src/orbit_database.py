from pathlib import Path
from orbit_database import Manager
from orbit_component_base.src.orbit_shared import world
from loguru import logger as log


class OrbitDatabase:

    PATH = 'default'
    FILE = None
    MAX_DATABASE_SIZE = 64
    COLLECTIONS = []
    CONFIG = {
        'map_size': 1024 * 1024 * 1024 * 64,
        'reindex': False,
        'auditing': True,
        'writemap': True
    }

    @property
    def real_path (self):
        return self._floc
    
    def __init__ (self):
        self._path = self.PATH
        self._file = self.FILE
        self._config = self.CONFIG
        self._floc = None
       
    def open(self):
        if self._path == 'default':
            path = world.conf.database
        elif path and self._file:
            path = Path(self._path) / self._file
        else:
            raise Exception(f'bad database specification: {self._path} / {self._file}')
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        self._manager = Manager()
        self._database = self._manager.database('db', path.as_posix(), config=self._config)
        self._floc = path.as_posix()
        return self
    
    def close (self):
        self._manager.close()

