import logging
from pathlib import Path

def get_logger(name):
    log_dir=Path(__file__).resolve().parent.parent/"logs"
    log_dir.mkdir(parents=True,exist_ok=True)
    logger=logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",datefmt= "%Y-%m-%d %H-%M-%S")
        
        file_handler=logging.FileHandler(log_dir/"openbmc_test_logs")
        file_handler.setFormatter(formatter)

        console_handler=logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


    return logger


    
