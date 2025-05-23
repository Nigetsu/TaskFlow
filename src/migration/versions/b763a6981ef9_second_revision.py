"""Second revision

Revision ID: b763a6981ef9
Revises: 50db0126663a
Create Date: 2025-05-05 18:33:41.350691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b763a6981ef9'
down_revision: Union[str, None] = '50db0126663a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_executors',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('task_id', 'user_id')
    )
    op.create_table('task_watchers',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('task_id', 'user_id')
    )
    op.drop_table('taskwatchers')
    op.drop_table('taskexecutors')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('taskexecutors',
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='taskexecutors_task_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='taskexecutors_user_id_fkey'),
    sa.PrimaryKeyConstraint('task_id', 'user_id', name='taskexecutors_pkey')
    )
    op.create_table('taskwatchers',
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='taskwatchers_task_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='taskwatchers_user_id_fkey'),
    sa.PrimaryKeyConstraint('task_id', 'user_id', name='taskwatchers_pkey')
    )
    op.drop_table('task_watchers')
    op.drop_table('task_executors')
    # ### end Alembic commands ###
