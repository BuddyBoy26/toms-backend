"""tenders updated 3

Revision ID: fc637c974fdd
Revises: e7d30d6455a9
Create Date: 2025-06-30 07:55:02.017179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc637c974fdd'
down_revision: Union[str, Sequence[str], None] = 'e7d30d6455a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1) Alter the column type, casting existing text to integer
    op.alter_column(
        'tenders', 'tender_id',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="tender_id::integer"
    )

    # 2) Create a sequence for auto-increment (if it doesn't already exist)
    op.execute(
        "CREATE SEQUENCE IF NOT EXISTS tenders_tender_id_seq OWNED BY tenders.tender_id"
    )

    # 3) Attach the sequence as default on tender_id
    op.execute(
        "ALTER TABLE tenders ALTER COLUMN tender_id SET DEFAULT nextval('tenders_tender_id_seq')"
    )

    # 4) Advance the sequence to the current max(tender_id)
    op.execute(
        "SELECT setval('tenders_tender_id_seq', GREATEST(MAX(tender_id),1)) FROM tenders"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # 1) Remove the default sequence
    op.execute(
        "ALTER TABLE tenders ALTER COLUMN tender_id DROP DEFAULT"
    )

    # 2) Drop the sequence
    op.execute(
        "DROP SEQUENCE IF EXISTS tenders_tender_id_seq"
    )

    # 3) Revert the column back to VARCHAR(50)
    op.alter_column(
        'tenders', 'tender_id',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )
