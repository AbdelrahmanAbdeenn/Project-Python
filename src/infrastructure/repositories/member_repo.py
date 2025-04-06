from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from src.domain.member_entity import Member
from src.infrastructure.database.schema import books, members
from src.infrastructure.repositories.base_repo import BaseRepo


class MemberRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)

    async def get_by_id(self, id: int | str, connection: AsyncConnection) -> Member | None:
        statement = select(self.table).where(self.table.c.id == id)
        result = await connection.execute(statement)
        row = result.fetchone()

        if not row:
            return None

        entity = self._map_row_to_entity(row)
        entity.books = await self._get_borrowed_books(id, connection)
        return entity

    async def _get_borrowed_books(self, id: int | str, connection: AsyncConnection) -> list[dict[str, Any]]:
        statement = select(
            books.c.id, books.c.title, books.c.author, books.c.borrowed_date
        ).where(books.c.borrowed_by == id)

        results = await connection.execute(statement)
        rows = results.fetchall()

        return [
            {
                'id': row.id,
                'title': row.title,
                'author': row.author,
                'borrowed_date': row.borrowed_date
            }
            for row in rows
        ]
