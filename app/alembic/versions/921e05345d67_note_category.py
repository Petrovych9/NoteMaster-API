"""note_category

Revision ID: 921e05345d67
Revises: 0327b6cd7fb1
Create Date: 2024-01-19 21:42:34.045496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '921e05345d67'
down_revision: Union[str, None] = '0327b6cd7fb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('notes', 'category',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)
    op.create_foreign_key(None, 'notes', 'notes_categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.alter_column('notes', 'category',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_table('notes_categories')
    # ### end Alembic commands ###