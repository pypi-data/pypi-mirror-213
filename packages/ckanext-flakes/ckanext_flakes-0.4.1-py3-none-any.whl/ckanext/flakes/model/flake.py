from __future__ import annotations

from collections import ChainMap
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from flatten_dict import flatten
from sqlalchemy import Column, DateTime, ForeignKey, UnicodeText, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import backref, relationship
from typing_extensions import Self

import ckan.model as model
from ckan.lib.dictization import table_dictize
from ckan.model.types import make_uuid

from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.orm import Query


class Flake(Base):
    __tablename__ = "flakes_flake"

    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    name: Optional[str] = Column(UnicodeText, unique=True, nullable=True)
    data: dict[str, Any] = Column(JSONB, nullable=False)
    modified_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    author_id: Optional[str] = Column(
        UnicodeText, ForeignKey(model.User.id), nullable=False
    )
    parent_id: Optional[str] = Column(UnicodeText, ForeignKey("flakes_flake.id"))
    extras: dict[str, Any] = Column(JSONB, nullable=False, default=dict)

    UniqueConstraint(name, author_id)

    author = relationship(
        model.User,
        backref=backref("flakes", cascade="all, delete"),
    )
    parent = relationship(
        "Flake",
        backref=backref("flakes", cascade="all, delete-orphan", single_parent=True),
        remote_side=[id],
    )

    def dictize(self, context: dict[str, Any]) -> dict[str, Any]:
        """Convert Flake into a serializable dictionary,

        If `expand` context flag is set, expand flake's data using the chaing
        of parent flakes.

        """
        result = table_dictize(self, context)

        if context.get("expand"):
            sources = [self.data]
            parent = self.parent

            while parent:
                sources.append(parent.data)
                parent = parent.parent

            result["data"] = dict(ChainMap(*sources))

        return result

    @classmethod
    def by_author(cls, author_id: Optional[str]) -> "Query[Self]":
        """Get user's flakes."""
        return model.Session.query(cls).filter_by(author_id=author_id)

    @classmethod
    def by_name(cls, name: str, author_id: Optional[str]) -> "Query[Self]":
        """Get user's flake using unique name of flake."""
        q = cls.by_author(author_id).filter_by(name=name)

        return q

    @classmethod
    def by_extra(
        cls, extras: dict[str, Any], author_id: Optional[str]
    ) -> "Query[Self]":
        """Get user's flakes using extra attribute."""
        flattened = flatten(extras)

        q = model.Session.query(cls)

        for k, v in flattened.items():
            key: Any = cls.extras
            for segment in k:
                key = key[segment]
            q = q.filter(key.astext == v)

        if author_id:
            q = q.filter(cls.author_id == author_id)

        return q
