"""Make hash columns unique and add columns to Kebechet app table

Revision ID: e7ebfc165a96
Revises: 2d7ef94ff4dd
Create Date: 2020-10-15 07:39:15.406208+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e7ebfc165a96"
down_revision = "2d7ef94ff4dd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "external_python_requirements", ["requirements_hash"])
    op.create_unique_constraint(None, "external_python_requirements_lock", ["requirements_lock_hash"])
    op.add_column(
        "kebechet_github_installations", sa.Column("advised_python_software_stack_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "kebechet_github_installations", sa.Column("external_python_software_stack_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "kebechet_github_installations", sa.Column("external_software_environment_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None,
        "kebechet_github_installations",
        "external_software_environment",
        ["external_software_environment_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "kebechet_github_installations",
        "external_python_software_stack",
        ["external_python_software_stack_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "kebechet_github_installations",
        "python_software_stack",
        ["advised_python_software_stack_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(None, "python_requirements", ["requirements_hash"])
    op.create_unique_constraint(None, "python_requirements_lock", ["requirements_lock_hash"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "python_requirements_lock", type_="unique")
    op.drop_constraint(None, "python_requirements", type_="unique")
    op.drop_constraint(None, "kebechet_github_installations", type_="foreignkey")
    op.drop_constraint(None, "kebechet_github_installations", type_="foreignkey")
    op.drop_constraint(None, "kebechet_github_installations", type_="foreignkey")
    op.drop_column("kebechet_github_installations", "external_software_environment_id")
    op.drop_column("kebechet_github_installations", "external_python_software_stack_id")
    op.drop_column("kebechet_github_installations", "advised_python_software_stack_id")
    op.drop_constraint(None, "external_python_requirements_lock", type_="unique")
    op.drop_constraint(None, "external_python_requirements", type_="unique")
    # ### end Alembic commands ###
