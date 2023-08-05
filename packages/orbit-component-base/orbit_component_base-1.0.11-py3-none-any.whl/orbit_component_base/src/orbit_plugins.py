from pkgutil import iter_modules
from sys import modules
from loguru import logger as log


class Plugins:

    PLUGIN_FOLDER = 'orbit_plugins'

    def __init__ (self, cls):
        self._cls = cls

    def __iter__ (self):
        tracker = set()
        for importer, package_name, _ in iter_modules():
            if package_name != 'orbit_component_base':
                continue
            full_package_name = f'{self.PLUGIN_FOLDER}.{package_name}'
            if full_package_name not in modules:
                plugin= importer.find_module(package_name).load_module(package_name)
                globals()[package_name] = plugin
            else:
                plugin = modules[full_package_name]
            if hasattr(plugin, self._cls):
                if full_package_name not in tracker:
                    tracker.add(full_package_name)
                    yield plugin

        for importer, package_name, _ in iter_modules([self.PLUGIN_FOLDER]):
            full_package_name = f'{self.PLUGIN_FOLDER}.{package_name}'
            if full_package_name not in modules:
                plugin= importer.find_module(package_name).load_module(package_name)
                globals()[package_name] = plugin
            else:
                plugin = modules[full_package_name]
            if hasattr(plugin, self._cls):
               if full_package_name not in tracker:
                    tracker.add(full_package_name)
                    yield plugin
                
        for importer, package_name, _ in iter_modules():
            if package_name.startswith('orbit_component'):
                full_package_name = f'{self.PLUGIN_FOLDER}.{package_name}'
                if full_package_name not in modules:
                    plugin= importer.find_module(package_name).load_module(package_name)
                    globals()[package_name] = plugin
                else:
                    plugin = modules[full_package_name]
                if hasattr(plugin, self._cls):
                    if full_package_name not in tracker:
                        tracker.add(full_package_name)
                        yield plugin
