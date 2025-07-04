import yaml
import random
import uuid
from datetime import datetime, timezone
import csv

def open_yaml(path):
    with open(path, 'r') as f:
        yaml_file = yaml.safe_load(f)
    return yaml_file


def validate_event(data, json_schema):
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

def generate_payment_record(user_ids, currency_ids):
   
   
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


def file_validator(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


