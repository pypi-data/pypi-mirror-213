from asyncio import CancelledError, Queue
from loguru import logger as log
from asyncio import create_task

class OrbitEmitter:
    
    def __init__ (self):
        self._emit = None
        self._queue = None

    def open (self, emit):
        self._emit = emit
        self._queue = Queue()
        create_task(self.async_task())

    async def emit (self, packet):
        self._queue.put_nowait(packet)
        
    async def async_task(self):
        while True:
            try:
                packet = await self._queue.get()
                sid = packet[1].get("sid")
                # log.success(f'EMIT: room={sid} {packet}')
                await self._emit(*packet, room=sid if sid else 'default')
            except CancelledError:
                log.debug('emit_queue_task handler was cancelled')
            except Exception as e:
                log.exception(e)
            