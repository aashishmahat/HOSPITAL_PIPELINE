import logging
import os

log_dir  = os.path.dirname(__file__)        # always saves to Logs/
log_file = os.path.join(log_dir, "pipeline.log")

def get_logger(name: str = "HospitalPipeline") -> logging.Logger:
    """Call this from any file: from Logs.logger_setup import get_logger"""
    logger = logging.getLogger(name)

    if logger.handlers:          # avoid adding duplicate handlers on reimport
        return logger

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s  [%(levelname)s]  %(message)s",
                             datefmt="%Y-%m-%d %H:%M:%S")

    # file handler — writes to Logs/pipeline.log
    fh = logging.FileHandler(log_file)
    fh.setFormatter(fmt)

    # console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger