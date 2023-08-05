from loguru import logger as log
from asyncio import sleep as async_sleep
from asyncio import get_event_loop
from time import time


class OutputBuffer:

    default_interval = 1.0

    def __init__(self, emitter):
        self._emitter = emitter
        self._flashpoints = {}

    async def run (self, model, flashpoint, delay=0):
        await async_sleep(delay)
        output = []
        for label in flashpoint.get('data'):
            response = {}
            if isinstance(flashpoint['data'][label], list):
                response['data'] = flashpoint['data'][label]
            else:
                response['data'] = [v for v in flashpoint['data'][label].values()]
                
            if response['data']:
                response['sid'] = flashpoint['sid']
                flashpoint['data'].update({label: {}})
                output.append(((f'{model}_{label}', response)))
        
        flashpoint['trigger'] = False
        for entry in output:
            await self._emitter.emit(entry)
        
                
    async def enqueue (self, sid, model, label, response):
        try:
            if 'ids' in response:
                await self._emitter.emit((f'{model}_{label}', response))
                return
            key = f'{sid}_{model}'
            if key not in self._flashpoints:
                self._flashpoints[key] = {'time': 0, 'trigger': None, 'sid': sid, 'data': {}}
            flashpoint = self._flashpoints[key]
            if label not in flashpoint['data']:
                flashpoint['data'][label] = {}
            
            if isinstance(response, dict):
                for item in response['data']:
                    flashpoint['data'][label][item['_id']] = item
            else:
                flashpoint['data'][label] = response
                
            if flashpoint['trigger']:
                return
            flush = flashpoint['time']
            delay = 0 if time() > flush else flush - time()
            if not delay:
                flashpoint['time'] = time() + self.default_interval
            flashpoint['trigger'] = True
            # log.debug(f"# RUN {key} :: {delay} :: {list(flashpoint['data'].keys())}")
            await get_event_loop().create_task(self.run(model, flashpoint, delay))
        except Exception as e:
            log.exception(e)
        

class InputBuffer:
    
    default_interval = 1.0
    
    def __init__(self, next):
        self._flashpoints = {}
        self._next = next
        
    async def run (self, model, flashpoint, delay):
        await async_sleep(delay)
        docs = flashpoint.get('docs', [])
        # log.success(f'FLUSH: {model} => {len(docs)}')
        flashpoint.update({'docs': [], 'trigger': False})
        await self._next(model, docs)

    async def enqueue (self, model, docs):
        # log.debug(f'incoming: {model} => {len(docs)}')
        if model not in self._flashpoints:
            self._flashpoints[model] = {'time': 0, 'trigger': False, 'docs': []}
        flashpoint = self._flashpoints[model]
        flashpoint['docs'] += docs
        if flashpoint['trigger']:
            # log.warning('triggered')
            return
        flush = flashpoint['time']
        delay = 0 if time() > flush else flush - time()
        if not delay:
            flashpoint['time'] = time() + self.default_interval
        flashpoint['trigger'] = True
        # log.debug(f'task: {model} => delay={delay}')
        await get_event_loop().create_task(self.run(model, flashpoint, delay))
