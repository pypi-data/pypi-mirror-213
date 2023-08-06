import dataclasses
import typing

from google.cloud.spanner_v1 import param_types

from sparta.spanner import DBService
from sparta.spanner.utils import zip_results

_LAST_UPDATED_AT = "last_updated_at"
_LAST_UPDATED_BY = "last_updated_by"
_CREATED_AT = "created_at"
_CREATED_BY = "created_by"
_UNMODIFIABLE_FIELDS = [_CREATED_AT, _CREATED_BY, _LAST_UPDATED_AT, _LAST_UPDATED_BY]


@dataclasses.dataclass
class ColumnMetadata:
    ordinal_position: int
    column_name: str
    spanner_type: str
    is_nullable: bool
    constraint_types: typing.List[str]


@dataclasses.dataclass
class TableMetadata:
    table_name: str
    table_pk: str
    table_pks: typing.List[str]
    columns_meta: typing.List[ColumnMetadata]
    unmodifiable_fields: typing.List[str]
    column_names: typing.List[str]


_SQL_METADATA = """SELECT ordinal_position, column_name, spanner_type, is_nullable, constraint_types
FROM (
    SELECT ordinal_position, column_name, spanner_type, is_nullable FROM information_schema.columns 
    WHERE table_name = @table_name
) LEFT OUTER JOIN (
    SELECT column_name, ARRAY_AGG(constraint_type) as constraint_types 
    FROM information_schema.KEY_COLUMN_USAGE
    JOIN information_schema.TABLE_CONSTRAINTS 
    USING (constraint_name, table_name)
    WHERE table_name = @table_name
    GROUP BY column_name
) USING (column_name)
ORDER BY ordinal_position"""


def _load_columns_meta(db: DBService, table_name: str) -> typing.List[ColumnMetadata]:
    assert table_name
    assert db
    params = {"table_name": table_name}
    ptypes = {
        "table_name": param_types.STRING,
    }
    result_set = db.execute_sql(
        sql=_SQL_METADATA,
        params=params,
        param_types=ptypes,
    )
    _list = zip_results(result_set)
    return [ColumnMetadata(**c) for c in _list]


def get_table_metadata(db: DBService, table_name: str) -> TableMetadata:
    assert table_name
    assert db
    columns_meta = _load_columns_meta(db, table_name)
    if not columns_meta:
        raise RuntimeError(f"No metadata for collection '{table_name}'")
    table_pks = [
        c.column_name
        for c in columns_meta
        if c.constraint_types and "PRIMARY KEY" in c.constraint_types
    ]
    if not table_pks:
        raise RuntimeError(f"Invalid metadata for collection '{table_name}'")
    elif len(table_pks) > 1:
        raise RuntimeError(
            f"Composite primary keys are not supported, yet (table_name: {table_name}, pks: {table_pks})"
        )
    unmodifiable_fields = table_pks + _UNMODIFIABLE_FIELDS
    column_names = [x.column_name for x in columns_meta]
    return TableMetadata(
        table_name=table_name,
        table_pk=table_pks[0],
        table_pks=table_pks,
        columns_meta=columns_meta,
        column_names=column_names,
        unmodifiable_fields=unmodifiable_fields,
    )
