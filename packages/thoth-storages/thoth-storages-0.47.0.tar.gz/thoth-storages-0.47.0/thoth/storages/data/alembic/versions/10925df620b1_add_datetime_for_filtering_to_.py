"""Add datetime for filtering to SecurityIndicatorAggregatedRun

Revision ID: 10925df620b1
Revises: 9aa4e29fa260
Create Date: 2020-07-07 10:46:35.292208+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10925df620b1"
down_revision = "9aa4e29fa260"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("si_aggregated_run", sa.Column("datetime", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("si_aggregated_run", "datetime")
    # ### end Alembic commands ###
