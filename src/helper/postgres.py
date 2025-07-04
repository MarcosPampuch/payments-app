import yaml
import psycopg2


class PostgresSQL:
    def __init__(self, dbname, user, password, host, port ) -> None:
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        # conn = psycopg2.connect(
        #     dbname="payments_db",
        #     user="admin",
        #     password="password1234",
        #     host="localhost",
        #     port=5433
        # )

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()


    def upsert_transaction(self, data) -> None:
        upsert_query = """
        INSERT INTO transactions (transaction_id, sender_user_id, receiver_user_id, amount, currency_id, transaction_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO UPDATE SET
            sender_user_id = EXCLUDED.sender_user_id,
            receiver_user_id = EXCLUDED.receiver_user_id,
            amount = EXCLUDED.amount,
            currency_id = EXCLUDED.currency_id,
            transaction_date = EXCLUDED.transaction_date,
            status = EXCLUDED.status;
        """

        self.cursor.execute(upsert_query, (
            data["transaction_id"],
            data["sender_id"],
            data["receiver_id"],
            data["amount"],
            data["currency_code"],
            data["timestamp"],
            data["status"]
        ))

    def get_user_ids(self):
        
        self.cursor.execute("SELECT DISTINCT user_id FROM users")
        user_ids = [row[0] for row in self.cursor.fetchall()]

        return user_ids
    
    def get_currency_ids(self):
        self.cursor.execute("SELECT DISTINCT currency_id FROM currencies")
        currency_ids = [row[0] for row in self.cursor.fetchall()]

        return currency_ids

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()