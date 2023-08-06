"""nullable_author

Revision ID: a7384c7e0e27
Revises: b8a5f5419306
Create Date: 2023-03-09 08:49:20.549623

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "a7384c7e0e27"
down_revision = "b8a5f5419306"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("flakes_flake", "author_id", nullable=True)


def downgrade():
    op.alter_column("flakes_flake", "author_id", nullable=False)
