import schedule
import time
from Logs.logger_setup import get_logger
from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import Storage_Choice
from report.reportgeneration import patient_report,doctor_patient

logger = get_logger("Scheduler")


def run_pipeline():
    logger.info("=== Pipeline Run Started ===")
    try:
        datasets     = load_datasets()
        cleaned_data = transforms_data(datasets)
        Storage_Choice(cleaned_data)
        patient_report(cleaned_data)
        doctor_patient(cleaned_data)
        logger.info("=== Pipeline Completed Successfully ===")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)


# ── Pick your schedule (uncomment ONE) ───────────────────────────────────────
# schedule.every().day.at("12:39").do(run_pipeline)     # daily at 6 PM
# schedule.every().day.at("00:00").do(run_pipeline)   # daily at midnight
# schedule.every(1).hours.do(run_pipeline)             # every hour
# schedule.every(10).minutes.do(run_pipeline)          # every 10 minutes
# schedule.every().monday.at("06:00").do(run_pipeline) # every Monday 6 AM
schedule.every(1).minutes.do(run_pipeline)
logger.info("Scheduler started. Waiting for scheduled runs...")

if __name__ == "__main__":
    logger.info("Scheduler started.")
    run_pipeline()                                    # run once on startup
    logger.info(f"Next run: {schedule.next_run()}")
    while True:
        schedule.run_pending()
        time.sleep(60)