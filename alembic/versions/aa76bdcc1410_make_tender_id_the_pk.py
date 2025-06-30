"""make tender_id the PK

Revision ID: aa76bdcc1410
Revises: 96c678e7543b
Create Date: 2025-06-30 09:22:42.277286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa76bdcc1410'
down_revision: Union[str, Sequence[str], None] = '96c678e7543b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1) Drop the old primary key constraint
    # op.drop_constraint("tenders_pkey", "tenders", type_="primary")
    # 2) (Optional) drop the old id column if you no longer need it:
    # op.drop_column("tenders", "id")
    # 3) Make tender_id the new primary key
    op.create_primary_key("tenders_pkey", "tenders", ["tender_id"])


def downgrade() -> None:
    """Downgrade schema."""
    pass
