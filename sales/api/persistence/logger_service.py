import json
import os
from datetime import datetime



class TransactionLoger:
    def __init__(self, file_path='logs/db_transactions.json'):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def log_transaction(self, sale):
        log_message = {
            'timestamp': datetime.now,
            'object': sale
        }
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(log_message) + '\n')
        
    
