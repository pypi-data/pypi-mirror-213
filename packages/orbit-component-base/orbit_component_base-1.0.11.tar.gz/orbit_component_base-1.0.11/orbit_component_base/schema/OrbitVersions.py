from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_component_base.schema.OrbitSessions import SessionsTable, SessionsCollection
from orbit_database import SerialiserType, Doc
from datetime import datetime
from loguru import logger as log


class VersionsTable (BaseTable):

    norm_table_name = 'versions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_product', 'func': '{product}'},
    ]

    @property
    def last_seen (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')

    def from_product (self, product, transaction=None):
        self.set(self.norm_tb.seek_one('by_product', Doc({'product': product}), txn=transaction))
        return self


class VersionsCollection (BaseCollection):

    table_class = VersionsTable
    table_methods = ['get_ids']

    async def get_version (self, product, version):
        log.error(f"!get_version: {product} => {version} => {self._ns}")
        vdoc = VersionsTable().from_product(product)
        if vdoc.isValid:
            doc = SessionsTable().from_sid(self._sid)
            if not doc.isValid:
                log.error(f'SESSION IS INVALID: {self._sid}')
                
                for result in SessionsCollection().filter('by_sid'):
                    log.info(result.doc._sid)
                                
                return {'ok': False, 'error': 'invalid session' }
            else:
                log.success(doc.doc)
                doc.update({'product': product, 'version': version}).save()
                log.warning(doc.doc)
            return {'ok': True, 'version': vdoc._version}
        return {'ok': False, 'error': 'Failed to find product in version table'}
