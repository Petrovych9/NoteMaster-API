"""initial

Revision ID: 8a1c77d6cc43
Revises: 
Create Date: 2024-01-24 22:55:07.472584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a1c77d6cc43'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Update existing rows with the default value
    op.execute("UPDATE notes SET category_id = 0 WHERE category_id IS NULL")
    # Commit the transaction before altering the column
    # Set the column to be non-nullable
    op.alter_column('notes', 'category_id', nullable=False)


    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.create_foreign_key('notes_category_fkey', 'notes', 'notes_categories', ['category'], ['id'])
    op.drop_column('notes', 'category_id')
    # ### end Alembic commands ###
