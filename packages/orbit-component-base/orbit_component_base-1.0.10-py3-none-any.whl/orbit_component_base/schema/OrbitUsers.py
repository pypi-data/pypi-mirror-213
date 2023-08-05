from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType


class UsersTable (BaseTable):

    norm_table_name = 'users'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON


class UsersCollection (BaseCollection):

    table_class = UsersTable
    table_strip = ['user_id']
