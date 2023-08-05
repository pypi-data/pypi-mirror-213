from loguru import logger as log
from orbit_database import Doc, AuditEntry
from orbit_component_base.src.orbit_nql_session import Session
from orbit_component_base.src.orbit_nql_buffer import InputBuffer, OutputBuffer
from orbit_component_base.src.orbit_nql_emitter import OrbitEmitter
from orbit_component_base.src.orbit_shared import world


class NQL:

    def __init__(self, emit, ns):
        self._emit = emit
        self._ns = ns
        self._methods = {}
        self._sessions = {}
        self._emitter = None
        self._output_buffer = None
        self._input_buffer = None

    def open (self):
        self._emitter = OrbitEmitter()
        self._output_buffer = OutputBuffer(self._emitter)
        self._input_buffer = InputBuffer(self.update_next)
        self._emitter.open(self._emit)
        return self

    def register(self, method_name, method):
        if not method:
            log.error(f'[programming error] unable to find routine "{method_name}" to publish')
        else:
            self._methods[method_name] = method
            log.success(f'Register: {method_name} for {self._ns}')

    def connect(self, sid):
        self._sessions[sid] = Session()
        self._sessions[sid].clear()

    def disconnect(self, sid):
        if sid in self._sessions:
            del self._sessions[sid]

    def call(self, sid, params):
        session = self._sessions[sid]
        model_name = params.get('model')
        label_name = params.get('label')
        if not model_name:
            return {'ok': False, 'error': f'no model for "{params}"'}
        if not label_name:
            return {'ok': False, 'error': f'no label for "{params}"'}

        try:
            cls, fn = self._methods.get(params.get('method'))
        except TypeError:
            fn = self._methods.get(params.get('method'))
            cls = None
        if not fn:
            error = f'missing method: {params.get("method")} ns={self._ns}'
            log.error(error)
            return {'ok': False, 'error': error}

        # log.debug(f"CALL2 || {params.get('method')} || fn=>{str(fn)}")

        if params.get('next', False):
            if 'ids' in params:
                # log.debug(f'Using old ids: {session.cache_params[model_name][label_name].get("ids", [])}')
                # log.debug(f'Plus  new ids: {params["ids"]}')
                old_ids = session.cache_params.get(model_name, {}).get(label_name, {}).get('ids', [])
                params['ids'] += old_ids
                session.cache_params[model_name][label_name]['ids'] = params['ids']
                # log.debug(f'Total IDS length={len(params["ids"])}')
            try:
                if cls:
                    result = fn(cls, session, params)
                else:
                    result = fn(session, params)
            except Exception as e:
                log.exception(e)
                return {'ok': False, 'error': str(e)}
            if isinstance(result, tuple):
                ids, data = result
                return {
                    'ok': True,
                    'ids': ids,
                    'data': data,
                }
            else:
                return result
        else:
            # log.debug(f"SETUP || {params.get('method')} || fn=>{str(fn)} || {params}")
            session.setup(params)
            old_set = set(session.cache_ids[model_name].get(label_name, []))
            try:
                if cls:
                    result = fn(cls, session, params)
                else:
                    result = fn(session, params)
                # log.success(f'OK: {str(result)}')
                # dref = session.verify(model_name)
                # dref = session.verify(model_name)
                # if dref:
                #     await self._output_buffer.enqueue(sid, model, '_invalidate', dref)
      
            except Exception as e:
                log.exception(e)
                return {'ok': False, 'error': str(e)}
            if isinstance(result, tuple):
                # log.debug(f"#1 {model_name} -> {label_name} => {fn}")
                # log.error(f'WORKING WITH A TUPLE: {str(result)}')
                ids, data = result
                # session.invalid_list[model_name] |= set(old_set) - set(ids)
                return {
                    'ok': True,
                    'ids': ids,
                    'data': data,
                    # 'dref': dref
                }
            else:
                if 'ids' in result:
                    # result['dref'] = dref
                    # session.invalid_list[model_name] |= set(old_set) - set(result['ids'])
                    return result
                log.debug("#3")
                return {
                    'ok': True,
                    'ids': [],
                    'data': [],
                    # 'dref': dref
                }

    def drop(self, sid, params):
        # log.warning(f"DROP: {params}")
        session = self._sessions[sid]
        model_name = params.get('model')
        label_name = params.get('label')
        if not model_name:
            return {'ok': False, 'error': f'no model for "{params}"'}
        if not label_name:
            return {'ok': False, 'error': f'no label for "{params}"'}
        return {'ok': True, 'data': session.flush(model_name, label_name)}
    
    def dump (self):
        data = {}
        for sid, session in dict(self._sessions).items():
            data[sid] = {}
            for model in session.cache_data:
                d = data[sid][model] = {}
                d['data_count'] = len(session.cache_data[model])
                for label in session.cache_ids[model]:
                    d[label] = len(session.cache_ids[model][label])
                
        return {'ok': True, 'data': data}

    async def send(self, model, docs):
        try:
            for doc in docs:
                await self._emitter.emit(doc)
        except Exception as e:
            log.exception(e)

    async def update(self, model, docs):
        if docs:
            await self._input_buffer.enqueue(model, docs)
        
    async def update_next (self, model, docs):
        try:
            for sid, session in dict(self._sessions).items():
                if model not in session.cache_ids:
                    continue
                for doc in docs:
                    if doc._e != AuditEntry.DELETE.value:
                        session.cache_data[model].discard(doc._o if isinstance(doc, Doc) else doc)
                for label in dict(session.cache_ids[model]):
                    params = dict(session.cache_params[model][label])
                    old_set = set(session.cache_ids[model].get(label, []))
                    count = params.get('count', 20)
                    if len(old_set) > count:
                        params['count'] = len(old_set)
                    if params.get('next'):
                        del params['next']
                    try:
                        cls, fn = self._methods.get(params.get('method'))
                    except TypeError:
                        fn = self._methods.get(params.get('method'))
                        cls = None
                    if not fn:
                        continue
                    try:
                        if cls:
                            # log.warning(f"Calling # 1: {sid} {params}")
                            result = fn(cls, session, params)
                        else:
                            log.warning(f"Calling # 2: {fn} {params}")
                            result = fn(session, params)
                    except Exception as e:
                        log.error(e)
                        return
                    if isinstance(result, tuple):
                        ids, data = result
                    else:
                        ids = result.get('ids')
                        data = result.get('data')
                    response = {'sid': sid}
                    if set(ids) != old_set:
                        response['ids'] = ids
                    if data:
                        response['data'] = data
                    if 'ids' in response or 'data' in response:
                        await self._output_buffer.enqueue(sid, model, label, response)
                dref = session.verify(model)
                if dref:
                    # log.error(f'Sending invalidate: {sid} => {model} => {dref}')
                    await self._output_buffer.enqueue(sid, model, '_invalidate', dref)
        except Exception as e:
            log.exception(e)
     

