from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_base.schema.OrbitVersions import VersionsCollection
from orbit_component_base.schema.OrbitSessions import SessionsCollection
from orbit_component_base.schema.OrbitUsers import UsersCollection
from loguru import logger as log


class Plugin (PluginBase):

    NAMESPACE = 'orbit'
    COLLECTIONS = [
        VersionsCollection,
        UsersCollection,
        SessionsCollection
    ]


class Args (ArgsBase):
        
    def setup (self):
        self._parser.add_argument("--dev", action='store_true', default=False, help='Start the Orbit server in development mode')
        self._parser.add_argument("--run", action='store_true', default=False, help='Start the Orbit server and run in the background')
        return super().process()
