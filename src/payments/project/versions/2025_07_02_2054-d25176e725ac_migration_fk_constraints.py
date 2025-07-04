"""migration_fk_constraints

Revision ID: d25176e725ac
Revises: 6002533e362f
Create Date: 2025-07-02 20:54:23.590881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd25176e725ac'
down_revision: Union[str, Sequence[str], None] = '6002533e362f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_foreign_key(
        'fk_sender_user_id',  
        'transactions',        
        'users',               
        ['sender_user_id'],    
        ['user_id'],           
        ondelete='CASCADE'     
    )

    
    op.create_foreign_key(
        'fk_receiver_user_id',  
        'transactions',         
        'users',                
        ['receiver_user_id'],   
        ['user_id'],            
        ondelete='CASCADE'      
    )

    
    op.create_foreign_key(
        'fk_currency_id',      
        'transactions',        
        'currencies',          
        ['currency_id'],       
        ['currency_id'],
        ondelete='SET NULL'    
    )

def downgrade() -> None:
   
    op.drop_constraint('fk_sender_user_id', 'transactions', type_='foreignkey')
    op.drop_constraint('fk_receiver_user_id', 'transactions', type_='foreignkey')
    op.drop_constraint('fk_currency_id', 'transactions', type_='foreignkey')
