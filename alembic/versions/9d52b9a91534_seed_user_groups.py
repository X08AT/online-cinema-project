"""seed user groups

Revision ID: 9d52b9a91534
Revises: 20bad690cf44
Create Date: 2026-09-20 21:31:33.108872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9d52b9a91534"
down_revision: Union[str, Sequence[str], None] = "20bad690cf44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        sa.table(
            "user_groups",
            sa.column("name", sa.String()),
        ),
        [
            {"name": "USER"},
            {"name": "MODERATOR"},
            {"name": "ADMIN"},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM user_groups "
            "WHERE name IN ('USER', 'MODERATOR', 'ADMIN')"
        )
    )