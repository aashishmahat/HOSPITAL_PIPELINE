from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import Storage_Choice
from report.reportgeneration import patient_report
from report.reportgeneration import doctor_patient
from Logs.logger_setup import get_logger

logger = get_logger()


def run_pipeline():
    logger.info("=== Pipeline Started ===")
    datasets     = load_datasets()
    cleaned_data = transforms_data(datasets)
    Storage_Choice(cleaned_data)
    patient_report(cleaned_data)
    doctor_patient(cleaned_data)
    logger.info("=== Pipeline Completed ===")


    
if __name__ == "__main__":
    run_pipeline()