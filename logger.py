import logging
import os

logging.basicConfig(level=logging.WARNING)

def get_logger(name: str, level: int) -> logging.Logger:
    if level not in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
        raise ValueError(f"Invalid logging level: {level}")
    
    
    log_file = f"{name}.log"
    log_path = os.path.join("logs", log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - Line: %(lineno)d - Stack: %(exc_info)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger