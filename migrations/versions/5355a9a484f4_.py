"""empty message

Revision ID: 5355a9a484f4
Revises: f284988cbaf9
Create Date: 2020-03-19 21:33:49.122823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5355a9a484f4'
down_revision = 'f284988cbaf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('person', sa.Column('firstname', sa.String(length=120), nullable=True))
    op.add_column('person', sa.Column('lastname', sa.String(length=120), nullable=True))
    op.add_column('person', sa.Column('zipcode', sa.String(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'zipcode')
    op.drop_column('person', 'lastname')
    op.drop_column('person', 'firstname')
    op.drop_column('person', 'address')
    # ### end Alembic commands ###