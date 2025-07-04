"""first_migration

Revision ID: aa7ac64b5ba5
Revises: 
Create Date: 2025-07-02 19:37:04.503971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP, DATE
from sqlalchemy import DECIMAL 


# revision identifiers, used by Alembic.
revision: str = 'aa7ac64b5ba5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.execute("""
        CREATE OR REPLACE FUNCTION update_modified_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.modified_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.create_table(
        'transactions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('transaction_id', UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('sender_user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('receiver_user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('amount', DECIMAL(10, 2), nullable=False),
        sa.Column('currency_id', sa.Integer, nullable=False),
        sa.Column('transaction_date', DATE, nullable=False),
        sa.Column('status', VARCHAR(20), nullable=False),
        sa.Column('created_at', TIMESTAMP, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('modified_at', TIMESTAMP, server_default=sa.func.current_timestamp(), nullable=False)
    )

    op.execute("""
        ALTER TABLE transactions
        ALTER COLUMN id SET DEFAULT gen_random_uuid();
    """)
    
    
    op.create_check_constraint(
        'status_check',
        'transactions',
        "status IN ('pending', 'completed', 'failed')"
    )


def downgrade() -> None:
    op.drop_table('transactions')
    op.execute("DROP FUNCTION IF EXISTS update_modified_at;")
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
