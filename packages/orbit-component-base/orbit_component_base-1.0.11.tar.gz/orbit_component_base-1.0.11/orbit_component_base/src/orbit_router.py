from aiohttp import web
from orbit_component_base.src.orbit_shared import world
from aiohttp import web, ClientSession, TCPConnector, client_exceptions
from loguru import logger as log

routes = web.RouteTableDef()


class OrbitRouter:

    def __init__(self, context=None, args=None):
        self._context = context
        self._args = args
        self._namespaces = set([])

    async def redirect(self, request):
        try:
            if not world.conf.web or world.args.dev:
                async with ClientSession(connector=TCPConnector(verify_ssl=False), skip_auto_headers=['accept-encoding']) as session:
                    origin = f"https://{world.conf.name}:{world.conf.vite_port}"
                    try:
                        async with session.get(f'{origin}{request.rel_url}') as resp:
                            headers = dict(resp.headers)
                            headers['Origin'] = origin
                            headers['Cache-Control'] = 'max-age=0, s-maxage=0'
                            return web.Response(body=await resp.content.read(), status=resp.status, headers=headers)
                    except client_exceptions.ClientConnectorError as e:
                        log.exception(e)
                        log.error(f'VITE server is down on: {origin}')
                        return ''
            else:
                path = (request.path if request.path != '/' else 'index.html').strip('/')
                headers = {'Cache-Control': 'max-age=0, s-maxage=0'}
                fullpath = world.conf.web / path
                log.debug(f'Delivering from filesystem: {fullpath.as_posix()}')
                return web.FileResponse(fullpath.as_posix(), headers=headers)
        except Exception as e:
            log.exception(e)
        return ''

    @web.middleware
    async def default_route(self, request, handler, *args):
        try:
            if request.path.strip('/') in self._namespaces:
                return await handler(request)
            return await self.redirect(request)
        except Exception as e:
            log.exception(e)

    def application(self):
        app = web.Application(middlewares=[self.default_route])
        app.add_routes(routes)
        return app
    
    def add_namespace (self, nsp):
        self._namespaces.add(nsp)
