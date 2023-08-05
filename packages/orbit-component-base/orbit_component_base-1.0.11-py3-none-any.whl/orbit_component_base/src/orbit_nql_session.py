from collections import defaultdict
from loguru import logger as log
from orbit_database import Doc


class Session:

    def __init__(self):
        self.clear()

    def has_context(self, params):
        return self.context_ids.get(params.get('model'), {}).get(params.get('label')) is not None

    def context(self, params):
        return self.context_ids.get(params.get('model'), {}).get(params.get('label'))

    def clear_context(self, params):
        self.context_ids[params.get('model')][params.get('label')] = defaultdict(dict)

    def next(self, params):
        return self.context_ids.get(params.get('model'), {}).get(params.get('label')) is not None

    def clear(self):
        # log.error("<<< CLEAR >>>")
        self.cache_data = defaultdict(set)
        # self.invalid_list = defaultdict(set)
        self.cache_ids = defaultdict(dict)
        self.cache_params = defaultdict(dict)
        self.context_ids = defaultdict(dict)
        # log.error('CLEAR CONTEXT IDS')

    def setup(self, params):
        label = params.get('label')
        model = params.get('model')
        self.cache_ids[model][label] = {}
        self.cache_params[model][label] = {}
        self.context_ids[model][label] = {}
        # log.error(f'Init Context IDS for model={model} label={label}')

    def kwargs(self, params):
        kwargs = {}
        if params.get('next'):
            kwargs['context'] = self.context_ids.get(params.get('model'), {}).get(params.get('label'))
        return kwargs

    def flush(self, model, label):
        # self.invalid_list[model] |= set(self.cache_ids[model].get(label, []))
        if label in self.cache_ids[model]:
            self.cache_ids[model][label] = {}
        return self.verify(model)

    def update(self, ids, params, context=None):
        model = params.get('model')
        label = params.get('label')
        if params.get('next') and model in self.cache_ids:
            self.cache_ids[model][label] += ids
            # log.error(f'=====> NOT saving params, model={model} label={label} params={str(params)}')
        else:
            self.cache_ids[model][label] = ids
            # log.error(f'=====> saving params, model={model} label={label} params={str(params)}')
            self.cache_params[model][label] = params
        # log.error(f'set context for model={model} label={label} || {context}')
        self.context_ids[model][label] = context

    def append(self, params, id, ids, data, result, strip=None, force=False):
        ids.append(id)
        model_name = params.get('model')
        if force or id not in self.cache_data.get(model_name, []):
            if not isinstance(result, Doc):
                result = result.doc
            data.append(result.doc_with_id if not strip else {k:v for (k,v) in result.doc_with_id.items() if k not in strip})
            try:
                self.cache_data[model_name].add(id)
                # if model_name == 'tagcount':
                #     log.error(f'{os.getpid()} => Sending {id} to "{model_name}" => {list(self.cache_data[model_name])}')
            except KeyError:
                log.error('<< CLIENT NEEDS TO RELOAD >>')

    def verify (self,model):
        referenced_ids = set.union(*[set(ids) for ids in self.cache_ids[model].values()])
        data_ids = self.cache_data[model]
        if referenced_ids.issubset(data_ids):
            # log.success(f'Model [{model}] integrity check')
            dref = data_ids.difference(referenced_ids)
            if dref:
                # log.success(f'IDS for "{model}" no longer referenced: {dref}')
                for id in dref:
                    self.cache_data[model].discard(id)
                # log.info(f'{model} dref: {dref}')
                return list(dref)
        else:
            log.critical('-------------------------------------')            
            log.error(f'Model [{model}] integrity check fail')
            log.warning(f'Data: {data_ids}')
            log.info(f'Refd: {referenced_ids}')
            for label in self.cache_ids[model]:
                log.warning(f'=> {label}: {set(self.cache_ids[model][label]).difference(set(data_ids))}')
                log.debug(f'=> {label}: {set(data_ids).difference(set(self.cache_ids[model][label]))}')
            log.warning(f'IDS no longer referenced: {data_ids.difference(referenced_ids)}')
            log.critical('-------------------------------------')
        return []
