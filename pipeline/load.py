import sqlalchemy
import pandas as pd
from pathlib import Path
from Logs.logger_setup import get_logger

logger    = get_logger()
LOAD_DATA = Path("cleaned_data")
DB_PATH   = Path("hospital.db")       # SQLite file saved in project root


def get_engine():
    return sqlalchemy.create_engine(f"sqlite:///{DB_PATH}")


TABLE_NAMES = {
    "patients":     "patients",
    "doctors":      "doctors",
    "department":   "departments",
    "admission":    "admissions",
    "appointments": "appointments",
    "billing":      "billing",
    "labTests":     "lab_tests",
    "diagnoses":    "diagnoses",
    "prescription": "prescriptions",
}


def store(cleaned_data: dict) -> None:
    # ── CSV backup ────────────────────────────────────────────────────────────
    LOAD_DATA.mkdir(exist_ok=True)
    for name, df in cleaned_data.items():
        df.to_csv(LOAD_DATA / f"{name}_cleaned.csv", index=False)
    logger.info("CSV backup saved to cleaned_data/")

    # ── SQLite load ───────────────────────────────────────────────────────────
    try:
        engine = get_engine()
        for name, df in cleaned_data.items():
            table = TABLE_NAMES.get(name, name)
            df.to_sql(name=table, con=engine, if_exists="replace",
                      index=False, chunksize=500)
            logger.info(f"  Loaded '{table}' → {len(df)} rows")
        logger.info(f"All datasets loaded into SQLite ({DB_PATH})")
    except Exception as e:
        logger.error(f"SQLite load failed: {e}", exc_info=True)