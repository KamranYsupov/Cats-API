"""initial

Revision ID: 43effe4ddb5c
Revises: 
Create Date: 2024-09-29 19:09:25.206493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43effe4ddb5c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('breeds',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_breeds'))
    )
    op.create_index(op.f('ix_breeds_id'), 'breeds', ['id'], unique=False)
    op.create_index(op.f('ix_breeds_name'), 'breeds', ['name'], unique=True)
    op.create_table('cats',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('age_months', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('breed_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['breed_id'], ['breeds.id'], name=op.f('fk_cats_breed_id_breeds'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cats'))
    )
    op.create_index(op.f('ix_cats_id'), 'cats', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cats_id'), table_name='cats')
    op.drop_table('cats')
    op.drop_index(op.f('ix_breeds_name'), table_name='breeds')
    op.drop_index(op.f('ix_breeds_id'), table_name='breeds')
    op.drop_table('breeds')
    # ### end Alembic commands ###
