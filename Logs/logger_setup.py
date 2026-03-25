import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR  = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")
FORMAT   = "%(asctime)s  [%(levelname)s]  %(name)s - %(message)s"


def get_logger(name: str = "HospitalPipeline") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:          # avoid duplicate handlers on re-import
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    # File handler — rotates at 5 MB, keeps 3 backups
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    fh.setFormatter(fmt)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger