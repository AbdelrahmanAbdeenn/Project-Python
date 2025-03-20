from dataclasses import dataclass
from typing import Any

from src.domain.base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    name: str
    email: str
    id: str | None = None
    books: list[dict[str, Any]] | None = None
