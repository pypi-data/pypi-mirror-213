from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType, Doc
from datetime import datetime


class SessionsTable (BaseTable):

    norm_table_name = 'sessions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_when'   , 'duplicates': True , 'func': '{when:14.6f}'},
        {'index_name': 'by_sid'    , 'duplicates': False, 'func': '{sid}', 'force': True},
        {'index_name': 'by_ns'     , 'duplicates': True,  'func': '{ns}'},
    ]

    def from_sid (self, sid, transaction=None):
        self.set(self.norm_tb.seek_one('by_sid', Doc({'sid': sid}), txn=transaction))
        return self

    @property
    def when (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')


class SessionsCollection (BaseCollection):

    table_class = SessionsTable
    table_strip = ['address', 'sid', 'user_id']

    def flush (self, nsp):
        limit = Doc({'ns': nsp})
        for result in self.filter(index_name='by_ns', lower=limit, upper=limit):
            result.doc.delete()
        return self

    def disconnect (self):
        session = SessionsTable().from_sid(self._sid)
        if session.isValid:
            session.delete()
