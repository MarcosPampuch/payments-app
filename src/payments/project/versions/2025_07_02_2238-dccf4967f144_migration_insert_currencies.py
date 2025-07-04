"""migration_insert_currencies

Revision ID: dccf4967f144
Revises: d6838548743d
Create Date: 2025-07-02 22:38:11.190525

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'dccf4967f144'
down_revision: Union[str, Sequence[str], None] = 'd6838548743d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Data to insert into currencies table
    currencies_data = [
        (840, 'USA', 'Dollar'),
        (978, 'EUR', 'Euro'),
        (608, 'PHP', 'Philippine Peso'),
        (344, 'HKD', 'Hong Kong Dollar'),
        (986, 'BRL', 'Real')
    ]

    # Using parameterized queries with sqlalchemy.text to avoid SQL injection risks
    for currency_id, currency, currency_name in currencies_data:
        session.execute(
            text("INSERT INTO currencies (currency_id, currency, currency_name) "
                 "VALUES (:currency_id, :currency, :currency_name)"),
            {'currency_id': currency_id, 'currency': currency, 'currency_name': currency_name}
        )

    # Commit the changes
    session.commit()


def downgrade() -> None:
    op.execute('DELETE FROM currencies')
