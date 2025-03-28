"""Make book id auto-increment

Revision ID: 83a52be019e7
Revises: c377659cee6e
Create Date: 2025-03-20 14:04:00.918488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '83a52be019e7'
down_revision: Union[str, None] = 'c377659cee6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'id', existing_type=sa.Integer(), autoincrement=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_borrowed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('borrowed_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('borrowed_by', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['borrowed_by'], ['members.id'], name='books_borrowed_by_fkey'),
    sa.PrimaryKeyConstraint('id', name='books_pkey')
    )
    op.create_table('members',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='members_pkey'),
    sa.UniqueConstraint('email', name='members_email_key')
    )
    # ### end Alembic commands ###
