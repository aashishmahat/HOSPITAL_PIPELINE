import schedule
import time
from Logs.logger_setup import get_logger
from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import store
from pipeline.report import generate_report

logger = get_logger("Scheduler")


def run_pipeline():
    logger.info("=== Pipeline Run Started ===")
    try:
        datasets     = load_datasets()
        cleaned_data = transforms_data(datasets)
        store(cleaned_data)
        generate_report()
        logger.info("=== Pipeline Completed Successfully ===")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)


# ── Pick your schedule (uncomment ONE) ───────────────────────────────────────
schedule.every().day.at("06:00").do(run_pipeline)     # daily at 6 AM
# schedule.every().day.at("00:00").do(run_pipeline)   # daily at midnight
# schedule.every(1).hours.do(run_pipeline)             # every hour
# schedule.every(10).minutes.do(run_pipeline)          # every 10 minutes
# schedule.every().monday.at("06:00").do(run_pipeline) # every Monday 6 AM


if __name__ == "__main__":
    logger.info("Scheduler started.")
    run_pipeline()                                    # run once on startup
    logger.info(f"Next run: {schedule.next_run()}")
    while True:
        schedule.run_pending()
        time.sleep(60)