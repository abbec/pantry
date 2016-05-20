"""empty message

Revision ID: 0e097717896a
Revises: None
Create Date: 2016-05-19 18:50:52.875427

"""

# revision identifiers, used by Alembic.
revision = '0e097717896a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('targets',
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(length=60), nullable=False),
    sa.Column('nickname', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=60), nullable=False),
    sa.Column('maintainer', sa.String(length=60), nullable=False),
    sa.Column('health_percent', sa.Integer(), nullable=True),
    sa.Column('state', sa.Enum('ready', 'leased', 'down', 'maintenance'), nullable=True),
    sa.PrimaryKeyConstraint('target_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('targets')
    ### end Alembic commands ###