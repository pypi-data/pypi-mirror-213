from orbit_database import Doc, WriteTransaction
from loguru import logger as log
from tqdm import tqdm


def register_class (cls):
    base = cls.table_class.norm_table_name
    cls._api = {}
    for name, entry in cls.__dict__.items():
        if callable(entry) and getattr(entry, 'orbit_published', None):
                cls._api[f'api_{base}_{name}'] = (cls, entry)
    return cls

def register_method (method):
    method.orbit_published = True
    return method


class BaseTable (Doc):

    norm_tb = None
    norm_auditing = True
    norm_codec = None
    norm_compression = None
    norm_table_name = None
    norm_ensure = []

    @property
    def isValid(self):
        return self.oid is not None

    @classmethod
    def reset(self, table):
        self.norm_tb = table
        return self

    def set(self, doc):
        if doc:
            self.dat = doc.doc
            self.oid = doc.oid
        return self

    def from_raw(self, raw, key=None):
        if key:
            self.oid = key if isinstance(key, bytes) else key.encode()
        self.dat = raw            
        return self

    def from_doc(self, doc):
        return self.set(doc)

    def from_key(self, key, transaction=None):
        return self.set(self.norm_tb.get(key, txn=transaction))

    def reload(self, transaction=None):
        return self.from_key(self.key, transaction=transaction)

    def exists(self, oid, transaction=None):
        return True if self.norm_tb.get(oid) else False

    def update(self, entry):
        self.upd = dict(self.upd, **{k:v for (k,v) in entry.items() if (not k.startswith('_') and entry.get(k) != self.doc.get(k))})
        return self

    def delete(self, transaction=None):
        if self.key:
            self.norm_tb.delete([self.key], txn=transaction)
        return self

    def append(self, transaction=None):
        self.norm_tb.append(self, txn=transaction)
        return self

    def save(self, transaction=None):
        if self.doc:
            self.norm_tb.save(self, txn=transaction) if self.oid else self.norm_tb.append(self, txn=transaction)
        return self

    def clone(self):
        self.oid = None
        return self

    def lookup_by_key(self, index_name, doc, transaction=None):
        self.set(self.norm_tb.seek_one(index_name, doc, txn=transaction))
        return self


class BaseCollection:

    _dbh = None
    _nql = None
    _api = {}

    table_class = None
    table_strip = None
    table_methods = []

    def __init__ (self, sid=None, session=None, ns=None):
        self._sid = sid
        self._session = session
        self._ns = ns

    def __iter__ (self, param=None):
        return self.table_class().norm_tb.filter()

    @property
    def write_transaction (self):
        return WriteTransaction(self._dbh._database)

    def open (self, dbh, nql=None, transaction=None):
        self.__class__._dbh = dbh
        self.__class__._nql = nql

        def open_table (transaction):
            kwargs = {
                'table_name': self.table_class.norm_table_name,
                'auditing': self.table_class.norm_auditing,
                'codec': self.table_class.norm_codec,
                'compression_type': self.table_class.norm_compression,
                'txn': transaction,
                'cls': self.table_class,
            }
            table = dbh._database.table(**kwargs)
            for spec in self.table_class.norm_ensure:
                if dbh._database.flag_reindex:
                    log.error(f'Forcing reindex: {self.table_class.norm_table_name}')
                    spec['force'] = True
                    with tqdm(total=table.records(txn=transaction), unit='') as progress:
                        progress.set_description(f'{self.table_class.norm_table_name + "/" + spec["index_name"]:30}')
                        table.ensure(**spec, progress=progress, txn=transaction)
                else:
                    table.ensure(**spec, txn=transaction)
            self.table_class.reset(table)
        if transaction:
            open_table(transaction)
        else:
            with self.write_transaction as transaction:
                open_table(transaction)
        if nql:
            for method in self.table_methods:
                nql.register(f'api_{self.table_class.norm_table_name}_{method}' , (self.__class__, getattr(self.__class__, method)))
            self.table_class.norm_tb.watch(callback=self.callback)
            for fn in self._api.keys():
                nql.register(fn, self._api[fn])

    async def callback(self, docs):
        try:
            await self._nql.update(self.table_class.norm_table_name, docs)
        except Exception as e:
            log.exception(e)
       
    def filter(self, *args, **kwargs):
        try:
            if self.table_class.norm_tb:
                return self.table_class.norm_tb.filter(*args, **kwargs)
            else:
                log.error(f'table not initialised: {self.table_name} // {self.table_class}')
                return []
        except Exception as e:
            log.exception(e)

    def records(self, transaction=None):
        return self.table_class.norm_tb.records()

    def empty(self, transaction=None):
        if self.table_class.norm_tb is not None:
            return self.table_class.norm_tb.empty(txn=transaction)
        return None

    def drop(self, index_name, transaction=None):
        return self.table_class.norm_tb.drop(index_name, txn=transaction)

    def drop_all(self, transaction=None):
        for index_name in list(self.table_class.norm_tb):
            self.table_class.norm_tb.drop(index_name, txn=transaction)
        return True

    def indexes(self, transaction=None):
        return list(self.table_class.norm_tb.indexes(txn=transaction))

    def first(self, transaction=None):
        return self.table_class.norm_tb.first()

    def get_ids(cls, session, params, transaction=None):
        ids, data = [], []
        if 'ids' in params:
            for id in params['ids']:
                if id:
                    doc = cls.table_class().from_key(id)
                    if doc.isValid:
                        session.append(params, doc.key, ids, data, doc, strip=cls.table_strip)
        else:
            for result in cls().filter(**params.get('filter')) if 'filter' in params else cls():
                session.append(params, result.oid.decode(), ids, data, result, strip=cls.table_strip)
        session.update(ids, params)
        return {'ok': True, 'ids': ids, 'data': data}
