from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import store
from pipeline.storage_choice import Storage_Choice
from report.reportgeneration import patient_report
from report.reportgeneration import doctor_patient
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def main():
    logging.info("Pipeline Execution Completed")
    print("=== Starting Hospital Analytics Pipeline ===\n")
    #Extract datasets
    logging.info("ETL process Started")
    datasets = load_datasets()
    #Transform datasets
    cleaned_data=transforms_data(datasets)
    #load data 
    store(cleaned_data)
    logging.info("ETL PROCESS END!")
    print("\n=== Pipeline Execution Completed ===")
    #storage choice 
    Storage_Choice(cleaned_data)
    #report generation
    patient_report(cleaned_data)
    doctor_patient(cleaned_data)

    
if __name__ == "__main__":
    main()