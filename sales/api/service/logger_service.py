from sales.api.entity.logger import logger

import json

def generate_result_log(response, type_log):
    response_data = json.loads(response.body.decode('utf-8'))
    
    log = {
        "success": response_data.get("success"),
        "timestamp": response_data.get("timestamp"),
        "status_code": response.status_code,
        "data": response_data
    }

    if type_log == 'info':
        logger.info(log)
    elif type_log == 'warning':
        logger.warning(log)
    elif type_log == 'error':
        logger.error(log)
        
    
