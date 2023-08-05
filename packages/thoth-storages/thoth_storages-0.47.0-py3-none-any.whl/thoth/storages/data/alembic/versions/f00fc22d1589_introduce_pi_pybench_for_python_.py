"""Introduce PI PyBench for Python Interpreter

Revision ID: f00fc22d1589
Revises: 3d0f03348c25
Create Date: 2019-12-16 12:40:36.344874+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f00fc22d1589"
down_revision = "3d0f03348c25"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pi_pybench",
        sa.Column("component", sa.String(length=256), nullable=False),
        sa.Column("origin", sa.String(length=256), nullable=False),
        sa.Column("version", sa.String(length=256), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("exit_code", sa.Integer(), nullable=False),
        sa.Column("ru_utime", sa.Float(), nullable=False),
        sa.Column("ru_stime", sa.Float(), nullable=False),
        sa.Column("ru_maxrss", sa.Integer(), nullable=False),
        sa.Column("ru_ixrss", sa.Integer(), nullable=False),
        sa.Column("ru_idrss", sa.Integer(), nullable=False),
        sa.Column("ru_isrss", sa.Integer(), nullable=False),
        sa.Column("ru_minflt", sa.Integer(), nullable=False),
        sa.Column("ru_majflt", sa.Integer(), nullable=False),
        sa.Column("ru_nswap", sa.Integer(), nullable=False),
        sa.Column("ru_inblock", sa.Integer(), nullable=False),
        sa.Column("ru_oublock", sa.Integer(), nullable=False),
        sa.Column("ru_msgsnd", sa.Integer(), nullable=False),
        sa.Column("ru_msgrcv", sa.Integer(), nullable=False),
        sa.Column("ru_nsignals", sa.Integer(), nullable=False),
        sa.Column("ru_nvcsw", sa.Integer(), nullable=False),
        sa.Column("ru_nivcsw", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("inspection_run_id", sa.Integer(), nullable=False),
        sa.Column("rounds", sa.Integer(), nullable=False),
        sa.Column("built_in_function_calls_average", sa.Float(), nullable=False),
        sa.Column("built_in_method_lookup_average", sa.Float(), nullable=False),
        sa.Column("compare_floats_average", sa.Float(), nullable=False),
        sa.Column("compare_floats_integers_average", sa.Float(), nullable=False),
        sa.Column("compare_integers_average", sa.Float(), nullable=False),
        sa.Column("compare_interned_strings_average", sa.Float(), nullable=False),
        sa.Column("compare_longs_average", sa.Float(), nullable=False),
        sa.Column("compare_strings_average", sa.Float(), nullable=False),
        sa.Column("compare_unicode_average", sa.Float(), nullable=False),
        sa.Column("concat_strings_average", sa.Float(), nullable=False),
        sa.Column("concat_unicode_average", sa.Float(), nullable=False),
        sa.Column("create_instances_average", sa.Float(), nullable=False),
        sa.Column("create_new_instances_average", sa.Float(), nullable=False),
        sa.Column("create_strings_with_concat_average", sa.Float(), nullable=False),
        sa.Column("create_unicode_with_concat_average", sa.Float(), nullable=False),
        sa.Column("dict_creation_average", sa.Float(), nullable=False),
        sa.Column("dict_with_float_keys_average", sa.Float(), nullable=False),
        sa.Column("dict_with_integer_keys_average", sa.Float(), nullable=False),
        sa.Column("dict_with_string_keys_average", sa.Float(), nullable=False),
        sa.Column("for_loops_average", sa.Float(), nullable=False),
        sa.Column("if_then_else_average", sa.Float(), nullable=False),
        sa.Column("list_slicing_average", sa.Float(), nullable=False),
        sa.Column("nested_for_loops_average", sa.Float(), nullable=False),
        sa.Column("normal_class_attribute_average", sa.Float(), nullable=False),
        sa.Column("normal_instance_attribute_average", sa.Float(), nullable=False),
        sa.Column("python_function_calls_average", sa.Float(), nullable=False),
        sa.Column("python_method_calls_average", sa.Float(), nullable=False),
        sa.Column("recursion_average", sa.Float(), nullable=False),
        sa.Column("second_import_average", sa.Float(), nullable=False),
        sa.Column("second_package_import_average", sa.Float(), nullable=False),
        sa.Column("second_submodule_import_average", sa.Float(), nullable=False),
        sa.Column("simple_complex_arithmetic_average", sa.Float(), nullable=False),
        sa.Column("simple_dict_manipulation_average", sa.Float(), nullable=False),
        sa.Column("simple_float_arithmetic_average", sa.Float(), nullable=False),
        sa.Column("simple_int_float_arithmetic_average", sa.Float(), nullable=False),
        sa.Column("simple_integer_arithmetic_average", sa.Float(), nullable=False),
        sa.Column("simple_list_manipulation_average", sa.Float(), nullable=False),
        sa.Column("simple_long_arithmetic_average", sa.Float(), nullable=False),
        sa.Column("small_lists_average", sa.Float(), nullable=False),
        sa.Column("small_tuples_average", sa.Float(), nullable=False),
        sa.Column("special_class_attribute_average", sa.Float(), nullable=False),
        sa.Column("special_instance_attribute_average", sa.Float(), nullable=False),
        sa.Column("string_mappings_average", sa.Float(), nullable=False),
        sa.Column("string_predicates_average", sa.Float(), nullable=False),
        sa.Column("string_slicing_average", sa.Float(), nullable=False),
        sa.Column("try_except_average", sa.Float(), nullable=False),
        sa.Column("try_raise_except_average", sa.Float(), nullable=False),
        sa.Column("tuple_slicing_average", sa.Float(), nullable=False),
        sa.Column("unicode_mappings_average", sa.Float(), nullable=False),
        sa.Column("unicode_predicates_average", sa.Float(), nullable=False),
        sa.Column("unicode_properties_average", sa.Float(), nullable=False),
        sa.Column("unicode_slicing_average", sa.Float(), nullable=False),
        sa.Column("totals_average", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["inspection_run_id"],
            ["inspection_run.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("pi_conv1d", sa.Column("component", sa.String(length=256), nullable=False))
    op.alter_column("pi_conv1d", "origin", existing_type=sa.VARCHAR(length=256), nullable=False)
    op.drop_column("pi_conv1d", "framework")
    op.add_column("pi_conv2d", sa.Column("component", sa.String(length=256), nullable=False))
    op.alter_column("pi_conv2d", "origin", existing_type=sa.VARCHAR(length=256), nullable=False)
    op.drop_column("pi_conv2d", "framework")
    op.add_column("pi_matmul", sa.Column("component", sa.String(length=256), nullable=False))
    op.alter_column("pi_matmul", "origin", existing_type=sa.VARCHAR(length=256), nullable=False)
    op.drop_column("pi_matmul", "framework")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("pi_matmul", sa.Column("framework", sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.alter_column("pi_matmul", "origin", existing_type=sa.VARCHAR(length=256), nullable=True)
    op.drop_column("pi_matmul", "component")
    op.add_column("pi_conv2d", sa.Column("framework", sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.alter_column("pi_conv2d", "origin", existing_type=sa.VARCHAR(length=256), nullable=True)
    op.drop_column("pi_conv2d", "component")
    op.add_column("pi_conv1d", sa.Column("framework", sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.alter_column("pi_conv1d", "origin", existing_type=sa.VARCHAR(length=256), nullable=True)
    op.drop_column("pi_conv1d", "component")
    op.drop_table("pi_pybench")
    # ### end Alembic commands ###
