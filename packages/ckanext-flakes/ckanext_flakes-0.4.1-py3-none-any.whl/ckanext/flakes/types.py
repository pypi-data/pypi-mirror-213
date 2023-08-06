from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from typing_extensions import NotRequired, TypedDict

D = TypeVar("D", bound=Mapping[str, Any])
E = TypeVar("E", bound=Mapping[str, Any])


class Flake:
    class Result:
        class Show(TypedDict, Generic[D, E]):
            id: str
            name: Optional[str]
            data: D
            modified_at: datetime
            author_id: str
            parent_id: Optional[str]
            extras: E

    class Payload:
        class Create(TypedDict, Generic[D, E]):
            name: NotRequired[str]
            data: D
            parent_id: NotRequired[str]
            extras: NotRequired[E]

        class Update(TypedDict, Generic[D, E]):
            id: str
            data: D
            parent_id: NotRequired[str]
            extras: NotRequired[E]

        class Override(TypedDict, Generic[D, E]):
            name: str
            data: D
            parent_id: NotRequired[str]
            extras: NotRequired[E]

        class Delete(TypedDict):
            id: str

        class Show(TypedDict):
            id: str
            expand: NotRequired[bool]

        _List = TypedDict("List", {"global": NotRequired[bool]})

        class List(_List, Generic[E]):
            user: NotRequired[str]
            expand: NotRequired[bool]
            # global: bool
            extras: NotRequired[E]

        class Lookup(TypedDict):
            name: str
            expand: NotRequired[bool]

        class Validate(TypedDict):
            id: str
            expand: NotRequired[bool]
            schema: str

        class Materialize(TypedDict):
            id: str
            expand: NotRequired[bool]
            remove: NotRequired[bool]
            action: str

        class Combine(TypedDict):
            id: str
            expand: NotRequired[dict[str, bool]]

        class Merge(TypedDict):
            id: str
            expand: NotRequired[dict[str, bool]]
            remove: NotRequired[bool]
            destination: NotRequired[str]

        class DataValidate(TypedDict):
            data: dict[str, Any]
            schema: str

        class DataExample(TypedDict):
            factory: str
            data: dict[str, Any]

        class DataPatch(TypedDict):
            id: str
            data: dict[str, Any]

        class ExtrasPatch(TypedDict):
            id: str
            extras: dict[str, Any]
