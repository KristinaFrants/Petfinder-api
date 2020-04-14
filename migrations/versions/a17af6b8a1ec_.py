"""empty message

Revision ID: a17af6b8a1ec
Revises: 
Create Date: 2020-04-03 22:09:44.139739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a17af6b8a1ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('petname', sa.String(length=20), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('message', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=True),
    sa.Column('lastname', sa.String(length=120), nullable=True),
    sa.Column('zipcode', sa.String(length=6), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('pet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('animal', sa.String(length=20), nullable=False),
    sa.Column('breed', sa.String(length=40), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('eyecolor', sa.String(length=20), nullable=True),
    sa.Column('furcolor', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pet')
    op.drop_table('person')
    op.drop_table('alert')
    # ### end Alembic commands ###