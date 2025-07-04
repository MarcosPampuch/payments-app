import yaml
import random
import uuid
from datetime import datetime, timezone
import csv

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


def validate_event(data: dict, json_schema: dict) -> bool:
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



