"""migration_indexes_and_triggers

Revision ID: 273007056863
Revises: d25176e725ac
Create Date: 2025-07-02 21:10:12.876901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '273007056863'
down_revision: Union[str, Sequence[str], None] = 'd25176e725ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TRIGGER transactions_update_modified_at_trigger
        BEFORE UPDATE ON transactions
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_at();
    """)

    op.execute("""
        CREATE TRIGGER users_update_modified_at_trigger
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_at();
    """)
   
   # transactions
    op.create_index('ix_transactions_transaction_id', 'transactions', ['transaction_id'])
    op.create_index('ix_transactions_transaction_date', 'transactions', ['transaction_date'])
    op.create_index('ix_transactions_sender_user_id', 'transactions', ['sender_user_id'])
    op.create_index('ix_transactions_receiver_user_id', 'transactions', ['receiver_user_id'])



def downgrade() -> None:

    # payments
    op.drop_index('ix_transactions_transaction_id', table_name='transactions')
    op.drop_index('ix_transactions_transaction_date', table_name='transactions')
    op.drop_index('ix_transactions_sender_user_id', table_name='transactions')
    op.drop_index('ix_transactions_receiver_user_id', table_name='transactions')


    
    op.execute("""
        DROP TRIGGER IF EXISTS users_update_modified_at_trigger ON users;
    """)

    op.execute("""
        DROP TRIGGER IF EXISTS transactions_update_modified_at_trigger ON transactions;
    """)
