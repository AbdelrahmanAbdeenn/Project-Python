"""Add users table

Revision ID: 835e2f796bd9
Revises:
Create Date: 2025-04-03 17:54:43.430357

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import uuid

# revision identifiers, used by Alembic.
revision: str = '835e2f796bd9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create 'members' table
    op.create_table(
        'members',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True)
    )

    # Create 'books' table
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('is_borrowed', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('borrowed_date', sa.DateTime(), nullable=True),
        sa.Column('borrowed_by', UUID(as_uuid=True), sa.ForeignKey('members.id'), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('books')
    op.drop_table('members')
