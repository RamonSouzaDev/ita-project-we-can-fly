import logging
import json
import sys
from datetime import datetime

class EngineeringLogger:
    """
    Professional Engineering Logger compliant with CREA-SP audit standards.
    Outputs structured JSON logs for machine parsing and standard logs for console.
    """
    
    @staticmethod
    def setup(name="ITA_AERO_SEC"):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if logger.hasHandlers():
            return logger

        # 1. Console Handler (Human Readable)
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(logging.INFO)
        c_format = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%H:%M:%S')
        c_handler.setFormatter(c_format)
        
        # 2. File Handler (JSON Audit Trail)
        f_handler = logging.FileHandler('flight_blackbox.jsonl')
        f_handler.setLevel(logging.DEBUG)
        
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_record = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": record.levelname,
                    "module": record.module,
                    "function": record.funcName,
                    "message": record.getMessage(),
                }
                return json.dumps(log_record)
        
        f_handler.setFormatter(JsonFormatter())
        
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
        return logger

logger = EngineeringLogger.setup()
