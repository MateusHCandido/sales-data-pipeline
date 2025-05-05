import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }
        if hasattr(record, "extra"):
            log_record["data"] = record.extra
        return json.dumps(log_record, ensure_ascii=False)

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"sales_log_{today}.json")

    logger = logging.getLogger("sales_logger")

    if not logger.hasHandlers():
        handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7, encoding="utf-8")
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger

logger = setup_logger()
