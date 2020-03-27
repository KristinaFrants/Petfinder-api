"""empty message

Revision ID: 3f191fc69ed5
Revises: a33c7fb83355
Create Date: 2020-03-27 19:30:16.935418

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3f191fc69ed5'
down_revision = 'a33c7fb83355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('alert_ibfk_1', 'alert', type_='foreignkey')
    op.drop_column('alert', 'person_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert', sa.Column('person_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('alert_ibfk_1', 'alert', 'person', ['person_id'], ['id'])
    # ### end Alembic commands ###