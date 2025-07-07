import yaml
import random
import uuid
from datetime import datetime, timezone
import csv
from helper.logger import logger

def open_yaml(path: str) -> dict:
    """
    Open a YAML file from the given path and return its contents as a dictionary.

    Args:
        path (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content as a dictionary.
    """
    with open(path, 'r') as f:
        yaml_file = yaml.safe_load(f)
    return yaml_file


def validate_payments_event(data: dict, json_schema: dict) -> bool:
    """
    Validate a data dictionary against a JSON schema dictionary.
    Returns True if the data matches the schema (including types and keys), False otherwise.

    Args:
        data (dict): The data to validate.
        json_schema (dict): The schema to validate against.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    
    if set(data.keys()) != set(json_schema.keys()):
        return False
    for key, typ in json_schema.items():
        
        expected_type = eval(typ)
        
        if expected_type == float and not isinstance(data[key], (float, int)):
            return False
        if expected_type != float and not isinstance(data[key], expected_type):
            return False
    return True

def generate_payment_record(user_ids: list, currency_ids: list) -> dict:
    """
    Generate a random payment record dictionary using provided user and currency IDs.

    Args:
        user_ids (list): List of user IDs.
        currency_ids (list): List of currency IDs.

    Returns:
        dict: A randomly generated payment record.
    """
    sender_id, receiver_id = random.sample(user_ids, 2)
    
    return {
        "transaction_id": str(uuid.uuid4()),
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "amount": round(random.uniform(500, 10000), 2),
        "currency_code": random.choice(currency_ids),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": random.choice(["pending", "failed", "completed"])
    }


def file_validator(filename: str) -> bool:
    """
    Check if the provided filename has a valid CSV extension.
    Returns True if valid, False otherwise.

    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if the file is a CSV, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


def format_imported_payment(data: dict, postgres_client) -> dict:
    """
    Validate imported payment data and return only the specified fields.
    
    Args:
        data (dict): The imported payment data to validate.
        postgres_client: PostgreSQL client object with get_user_id_from_username method.
        
    Returns:
        dict: A dictionary containing only the validated fields:
            - sender_id (int)
            - receiver_id (int)
            - amount (float)
            - currency (string)
            - transaction_date (timestamp)
            - status (string)
    """
    
    required_fields = {
        'username_sender': str,
        'username_receiver': str,
        'amount': (float, int), 
        'currency': str,
        'transaction_date': str,  
        'status': str
    }
    
    validated_data = {}
    
    for field, expected_type in required_fields.items():
        if field not in data:
            return None 
            
        value = data[field]
        

        if field == 'amount':
            if not isinstance(value, (float, int)):
                return None
            validated_data[field] = float(value)
        else:
            if not isinstance(value, expected_type):
                return None
            if field not in ('username_sender', 'username_receiver', 'currency'):
                validated_data[field] = value
    
    
    sender_id, receiver_id = postgres_client.get_user_id_from_username(sender=data['username_sender'], 
                                                                       receiver=data['username_receiver'])
    
    if not sender_id or not receiver_id:
        return None
    else:
        validated_data['sender_id'] = sender_id
        validated_data['receiver_id'] = receiver_id
    
    

    currency_code = postgres_client.get_currency_code_from_currency(currency=data['currency'])

    if not currency_code:
        return None
    else:
        validated_data['currency_code'] = currency_code

    return validated_data



