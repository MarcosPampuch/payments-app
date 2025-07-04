import yaml
import psycopg2


class PostgresSQL:
    """
    PostgreSQL client wrapper for connecting, querying, and upserting transactions.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        """
        Initialize the PostgresSQL client and connect to the database.

        Args:
            dbname (str): Database name.
            user (str): Username.
            password (str): Password.
            host (str): Host address.
            port (str): Port number.
        """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()


    def upsert_transaction(self, data: dict) -> None:
        """
        Insert or update a transaction record in the transactions table using the provided data dictionary.

        Args:
            data (dict): Transaction data to upsert.
        """
        
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

    def get_user_ids(self) -> list:
        """
        Retrieve all distinct user_id values from the users table.

        Returns:
            list: List of user IDs.
        """

        self.cursor.execute("SELECT DISTINCT user_id FROM users")
        user_ids = [row[0] for row in self.cursor.fetchall()]

        return user_ids
    
    def get_currency_ids(self) -> list:
        """
        Retrieve all distinct currency_id values from the currencies table.

        Returns:
            list: List of currency IDs.
        """
        self.cursor.execute("SELECT DISTINCT currency_id FROM currencies")
        currency_ids = [row[0] for row in self.cursor.fetchall()]

        return currency_ids

    def close(self) -> None:
        """
        Close the database cursor and connection.
        """
        self.cursor.close()
        self.conn.close()