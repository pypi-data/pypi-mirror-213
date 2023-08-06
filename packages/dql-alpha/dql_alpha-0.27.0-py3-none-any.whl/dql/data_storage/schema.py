from typing import TYPE_CHECKING, Generic, List, Optional, Sequence, Type, TypeVar

import sqlalchemy as sa
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    Text,
)
from sqlalchemy.sql.expression import true

from dql.node import DirTypeGroup

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.sql.base import Executable
    from sqlalchemy.sql.selectable import Select


class Table:
    def __init__(self, name: str, metadata: Optional["MetaData"] = None):
        self.metadata: "MetaData" = metadata if metadata is not None else MetaData()
        self.name: str = name
        self.table: "sa.Table" = self.get_table()

    @property
    def columns(self) -> List[Column]:
        return self.table.columns

    @property
    def c(self):
        return self.columns

    @classmethod
    def default_columns(cls) -> List[Column]:
        return []

    @property
    def custom_columns(self):
        """List of custom columns added to the table."""
        default_cols = [c.name for c in self.default_columns()]
        return [c for c in self.columns if c.name not in default_cols]

    def get_table(self) -> "sa.Table":
        table = self.metadata.tables.get(self.name)
        if table is None:
            table = sa.Table(
                self.name,
                self.metadata,
                *self.default_columns(),
            )
        return table

    def apply_conditions(self, query: "Executable") -> "Executable":
        """
        Apply any conditions that belong on all selecting queries.

        This could be used to filter tables that use access control.
        """
        return query

    def select(self, *columns):
        if not columns:
            query = self.table.select()
        else:
            query = sa.select(*columns).select_from(self.table)
        return self.apply_conditions(query)

    def insert(self):
        return self.table.insert()

    def update(self):
        return self.apply_conditions(self.table.update())

    def delete(self):
        return self.apply_conditions(self.table.delete())


class BaseDatasetRow(Table):
    @classmethod
    def default_columns(cls) -> List[Column]:
        return [
            Column("id", Integer, primary_key=True),
            Column("vtype", Text, nullable=False, index=True),
            Column("dir_type", Integer, index=True),
            Column("parent_id", Integer, index=True),
            Column("name", Text, nullable=False, index=True),
            Column("checksum", Text),
            Column("etag", Text),
            Column("version", Text),
            Column("is_latest", Boolean),
            Column("last_modified", DateTime),
            Column("size", BigInteger, nullable=False, index=True),
            Column("owner_name", Text),
            Column("owner_id", Text),
            Column("path_str", Text, index=True),
            Column("anno", JSON),
            Column("random", BigInteger, nullable=False),
            Column("location", JSON),
        ]

    @staticmethod
    def copy_signal_column(column: Column):
        """
        Copy a sqlalchemy Column object intended for use as a signal column.

        This does not copy all attributes as certain attributes such as
        table are too context-dependent and the purpose of this function is
        adding a signal column from one table to another table.

        We can't use Column.copy() as it only works in certain contexts.
        See https://github.com/sqlalchemy/sqlalchemy/issues/5953
        """
        return Column(
            column.name,
            column.type,
            primary_key=column.primary_key,
            index=column.index,
            nullable=column.nullable,
            default=column.default,
            server_default=column.server_default,
            unique=column.unique,
        )

    @classmethod
    def new_table(
        cls,
        name: str,
        custom_columns: Sequence["Column"] = (),
        metadata: Optional["MetaData"] = None,
    ):
        # copy columns, since re-using the same objects from another table
        # may raise an error
        custom_columns = [cls.copy_signal_column(c) for c in custom_columns]
        if metadata is None:
            metadata = MetaData()
        return sa.Table(
            name,
            metadata,
            *cls.default_columns(),
            *custom_columns,
        )


class Node(BaseDatasetRow):
    def __init__(self, name: str, source: str, metadata: Optional["MetaData"] = None):
        super().__init__(name, metadata=metadata)
        self.source = source

    @classmethod
    def default_columns(cls) -> List[Column]:
        return [
            *super().default_columns(),
            Column("partial_id", Integer),
            Column("valid", Boolean, default=True, nullable=False),
        ]

    def dataset_query(
        self,
        *column_names: str,
    ) -> "Select":
        if not column_names:
            column_names = DATASET_CORE_COLUMN_NAMES
        column_objects = [
            sa.literal(self.source).label("source") if c == "source" else self.c[c]
            for c in column_names
        ]
        # include all object types - file, tar archive, tar file (subobject)
        return self.select(*column_objects).where(
            self.c.dir_type.in_(DirTypeGroup.FILE)
            & (self.c.valid == true())
            & (self.c.is_latest == true())
        )


class DatasetRow(BaseDatasetRow):
    def __init__(
        self, name: str, engine: "Engine", metadata: Optional["MetaData"] = None
    ):
        self.engine = engine
        super().__init__(name, metadata)

    def get_table(self) -> "sa.Table":
        table = self.metadata.tables.get(self.name)
        if table is None:
            return sa.Table(
                self.name,
                self.metadata,
                extend_existing=True,
                autoload_with=self.engine,
            )
        return table

    @classmethod
    def default_columns(cls) -> List[Column]:
        return [
            *super().default_columns(),
            Column("source", Text, nullable=False),
        ]


DATASET_CORE_COLUMN_NAMES = tuple([col.name for col in DatasetRow.default_columns()])

NodeT = TypeVar("NodeT", bound=Node)
DatasetRowT = TypeVar("DatasetRowT", bound=DatasetRow)


class Schema(Generic[NodeT, DatasetRowT]):
    node_cls: Type[NodeT]
    dataset_row_cls: Type[DatasetRowT]


class DefaultSchema(Schema[Node, DatasetRow]):
    def __init__(self):
        self.node_cls = Node
        self.dataset_row_cls = DatasetRow
