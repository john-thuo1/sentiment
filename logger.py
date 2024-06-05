import logging
import os

def setup_logger(logger_file: str, log_dir: str = 'Logs', level=logging.INFO, 
                 format='%(asctime)s - %(levelname)s - %(message)s') -> logging.Logger:
    
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(log_dir, f'{logger_file}.log'), 
                        level=level, 
                        format=format)
    return logging.getLogger(logger_file)