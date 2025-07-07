import yaml
import psycopg2
from helper.logger import logger


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


    def upsert_transaction(self, data: dict, imported_transaction=False) -> None:
        """
        Insert or update a transaction record in the transactions table using the provided data dictionary.

        Args:
            data (dict): Transaction data to upsert.
        """
        
        if imported_transaction:
            upsert_query = """
            INSERT INTO transactions (sender_user_id, receiver_user_id, amount, currency_id, transaction_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(upsert_query, (
                data["sender_id"],
                data["receiver_id"],
                data["amount"],
                data["currency_code"],
                data["transaction_date"],
                data["status"]
            ))
        else:
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
    
    def get_user_id_from_username(self, sender:str, receiver:str) -> tuple:
        """
        Retrieve the receiver and sender users_id based on the username.

        Args:
            sender (str): Sender username
            receiver (str): Receiver username

        Returns:
            tuple: tuple containing (sender_id, receiver_id).
        """
        sender_user_id = None
        receiver_user_id = None

        # Get sender user_id
        self.cursor.execute(f"SELECT DISTINCT user_id FROM users WHERE username = '{sender}'")
        sender_result = self.cursor.fetchall()
        if sender_result:
            sender_user_id = sender_result[0][0]
        else:
            logger.error(f"Sender username '{sender}' not found in users table")

        # Get receiver user_id
        self.cursor.execute(f"SELECT DISTINCT user_id FROM users WHERE username = '{receiver}'")
        receiver_result = self.cursor.fetchall()
        if receiver_result:
            receiver_user_id = receiver_result[0][0]
        else:
            logger.error(f"Receiver username '{receiver}' not found in users table")

        return (sender_user_id, receiver_user_id)
    
    def get_currency_ids(self) -> list:
        """
        Retrieve all distinct currency_id values from the currencies table.

        Returns:
            list: List of currency IDs.
        """
        self.cursor.execute("SELECT DISTINCT currency_id FROM currencies")
        currency_ids = [row[0] for row in self.cursor.fetchall()]

        return currency_ids
    
    def get_currency_code_from_currency(self, currency:str) -> int:
        """
        Retrieve currency code from currency name in table currencies.

        Returns:
            integer: currency code number.
        """
        
        currency_code = None

        self.cursor.execute(f"SELECT currency_id FROM currencies WHERE currency='{currency}'")
        currency_result = self.cursor.fetchall()
        if currency_result:
            currency_code = currency_result[0][0]
        else:
            logger.error(f"Currency '{currency}' not found in currency table")


        return currency_code

    def close(self) -> None:
        """
        Close the database cursor and connection.
        """
        self.cursor.close()
        self.conn.close()