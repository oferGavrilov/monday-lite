"""
Central declarative base & metadata helpers.
"""

from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import MetaData

# —— naming convention keeps Alembic diffs deterministic ——
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class CustomBase:
    """Adds `__tablename__` automatically."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__tablename__.lower()


Base = declarative_base(cls=CustomBase, metadata=metadata)
