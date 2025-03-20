from typing import Any

from sqlalchemy import Connection, select

from src.domain.member_entity import Member
from src.infrastructure.database.schema import books, members
from src.infrastructure.repositories.base_repo import BaseRepo


class MemberRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)

    def get_by_id(self, id: int | str, connection: Connection) -> Member | None:
        statement = select(self.table).where(self.table.c.id == id)
        result = connection.execute(statement).fetchone()

        if not result:
            return None

        entity = self._map_row_to_entity(result)
        entity.books = self._get_borrowed_books(id, connection)
        return entity

    def _get_borrowed_books(self, id: int | str, connection: Connection) -> list[dict[str, Any]]:
        statement = select(
            books.c.id, books.c.title, books.c.author, books.c.borrowed_date
        ).where(books.c.borrowed_by == id)

        results = connection.execute(statement).fetchall()

        return [
            {
                'id': row.id,
                'title': row.title,
                'author': row.author,
                'borrowed_date': row.borrowed_date
            }
            for row in results
        ]
