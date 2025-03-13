from sqlalchemy import Column, Integer, String, Table , Boolean , DateTime , ForeignKey

from src.infrastructure.database.db import engine, metadata

books = Table('books', metadata,
    Column('book_id', Integer, primary_key=True,),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('is_borrowed', Boolean, default=False),
    Column('borrowed_date', DateTime, default=None),
    Column('borrowed_by', Integer, ForeignKey('members.member_id'), nullable=True)
)
# UUID NOT INTERER

members = Table('members', metadata,
    Column('member_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False, unique=True)
)
metadata.create_all(engine)