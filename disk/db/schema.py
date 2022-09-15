from sqlalchemy import MetaData
from enum import Enum, unique

from sqlalchemy import (
    Column, DateTime, Enum as PgEnum, ForeignKey, Integer, Table, String
)
from sqlalchemy.dialects.postgresql import UUID


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)


@unique
class FileType(Enum):
    file = 'FILE'
    folder = 'FOLDER'


files_table = Table(
    'files',
    metadata,
    Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    ),
    Column('type', PgEnum(FileType, name='file_type'), nullable=False),
    Column('url', String),
    Column('size', Integer, nullable=False),
    Column('parent_id', UUID(as_uuid=True), ForeignKey('files.id'), nullable=True),
    Column('update_date', DateTime, nullable=False),
)
