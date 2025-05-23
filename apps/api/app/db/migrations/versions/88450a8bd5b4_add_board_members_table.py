"""Add board_members table

Revision ID: 88450a8bd5b4
Revises:
Create Date: 2025-05-10 16:42:07.380535

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '88450a8bd5b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table(
        'boards',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['owner_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_boards_user_order', 'boards', ['owner_id', 'order'], unique=False
    )
    op.create_table(
        'refreshtokens',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_refresh_tokens_token', 'refreshtokens', ['token'], unique=False)
    op.create_index(
        'ix_refresh_tokens_user_expires',
        'refreshtokens',
        ['user_id', 'expires_at'],
        unique=False,
    )
    op.create_index(
        op.f('ix_refreshtokens_token'), 'refreshtokens', ['token'], unique=True
    )
    op.create_table(
        'boardmembers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('board_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.Enum('owner', 'member', name='roleenum'), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['board_id'],
            ['boards.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'tables',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('board_id', sa.UUID(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['board_id'],
            ['boards.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_tables_board_order', 'tables', ['board_id', 'order'], unique=False
    )
    op.create_table(
        'rows',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('table_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column(
            'status',
            sa.Enum('todo', 'in_progress', 'done', name='statusenum'),
            nullable=False,
        ),
        sa.Column(
            'priority',
            sa.Enum('low', 'medium', 'high', name='priorityenum'),
            nullable=False,
        ),
        sa.Column('assignee_id', sa.UUID(), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['assignee_id'],
            ['users.id'],
        ),
        sa.ForeignKeyConstraint(
            ['table_id'],
            ['tables.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rows_table_order', 'rows', ['table_id', 'order'], unique=False)
    op.create_table(
        'notes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('row_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['row_id'],
            ['rows.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_notes_row_created', 'notes', ['row_id', 'created_at'], unique=False
    )
    op.create_table(
        'notifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('row_id', sa.UUID(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['row_id'],
            ['rows.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    op.drop_index('ix_notes_row_created', table_name='notes')
    op.drop_table('notes')
    op.drop_index('ix_rows_table_order', table_name='rows')
    op.drop_table('rows')
    op.drop_index('ix_tables_board_order', table_name='tables')
    op.drop_table('tables')
    op.drop_table('boardmembers')
    op.drop_index(op.f('ix_refreshtokens_token'), table_name='refreshtokens')
    op.drop_index('ix_refresh_tokens_user_expires', table_name='refreshtokens')
    op.drop_index('ix_refresh_tokens_token', table_name='refreshtokens')
    op.drop_table('refreshtokens')
    op.drop_index('ix_boards_user_order', table_name='boards')
    op.drop_table('boards')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
