from orbit_component_base.src.orbit_orm import BaseCollection
from orbit_component_base.schema.OrbitSessions import SessionsTable as BaseTable
from orbit_database import Doc
from datetime import datetime


class SessionsTable (BaseTable):

    def from_sid (self, sid, transaction=None):
        self.set(self.norm_tb.seek_one('by_sid', Doc({'sid': sid}), txn=transaction))
        return self

    @property
    def when (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')


class SessionsCollection (BaseCollection):

    table_class = SessionsTable
    table_strip = ['address', 'sid', 'user_id']
    table_methods = ['get_ids']

    def disconnect (self):
        session = SessionsTable().from_sid(self._sid)
        if session.isValid:
            session.delete()
