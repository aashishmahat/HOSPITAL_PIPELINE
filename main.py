from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import store
from pipeline.report import generate_report
from Logs.logger_setup import get_logger

logger = get_logger()


def run_pipeline():
    logger.info("=== Pipeline Started ===")
    datasets     = load_datasets()
    cleaned_data = transforms_data(datasets)
    store(cleaned_data)
    generate_report()
    logger.info("=== Pipeline Completed ===")


    
if __name__ == "__main__":
    run_pipeline()