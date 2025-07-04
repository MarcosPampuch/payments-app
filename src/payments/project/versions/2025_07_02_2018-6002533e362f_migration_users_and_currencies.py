"""migration_users_and_currencies

Revision ID: 6002533e362f
Revises: aa7ac64b5ba5
Create Date: 2025-07-02 20:18:36.605819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP, DATE, BOOLEAN
from sqlalchemy import DECIMAL 


revision: str = '6002533e362f'
down_revision: Union[str, Sequence[str], None] = 'aa7ac64b5ba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('name', VARCHAR(200), nullable=False),
        sa.Column('email', VARCHAR(200), nullable=False),
        sa.Column('username', VARCHAR(200), nullable=False), 
        sa.Column('password', VARCHAR(200), nullable=False), 
        sa.Column('user_creation_date', TIMESTAMP, nullable=False),
        sa.Column('active', BOOLEAN, nullable=False),
        sa.Column('created_at', TIMESTAMP, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('modified_at', TIMESTAMP, server_default=sa.func.current_timestamp(), nullable=False)
    )
    
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN id SET DEFAULT gen_random_uuid();
    """)
    
    op.create_table(
        'currencies',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('currency_id', sa.Integer, nullable=False, unique=True),  
        sa.Column('currency', VARCHAR(20), nullable=False),
        sa.Column('currency_name', VARCHAR(50), nullable=False),
        sa.Column('created_at', TIMESTAMP, server_default=sa.func.current_timestamp(), nullable=False),  
    )

    op.execute("""
        ALTER TABLE currencies
        ALTER COLUMN id SET DEFAULT gen_random_uuid();
    """)

def downgrade() -> None:
    
    op.drop_table('currencies')
    
    
    op.drop_table('users')
