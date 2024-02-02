"""create user table

Revision ID: 14331f1a1be1
Revises: 
Create Date: 2024-02-02 05:00:31.617619

"""

from typing import Sequence, Union
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "14331f1a1be1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
