"""init tables

Revision ID: 764c5571e96e
Revises: 
Create Date: 2023-01-03 09:28:53.086943

"""
from alembic import op
import fastapi_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '764c5571e96e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', fastapi_utils.guid_type.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', fastapi_utils.guid_type.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', fastapi_utils.guid_type.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('user')
    # ### end Alembic commands ###