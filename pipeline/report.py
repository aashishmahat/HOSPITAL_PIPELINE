import pandas as pd
from pathlib import Path
from datetime import datetime
from Logs.logger_setup import get_logger

logger      = get_logger()
CLEANED_DIR = Path("cleaned_data")
REPORT_DIR  = Path("reports")


def load_cleaned() -> dict:
    files = {
        "patients":     "patients_cleaned.csv",
        "doctors":      "doctors_cleaned.csv",
        "appointments": "appointments_cleaned.csv",
        "billing":      "billing_cleaned.csv",
        "admission":    "admission_cleaned.csv",
        "labTests":     "labTests_cleaned.csv",
        "diagnoses":    "diagnoses_cleaned.csv",
        "prescription": "prescription_cleaned.csv",
        "department":   "department_cleaned.csv",
    }
    data = {}
    for name, fname in files.items():
        path = CLEANED_DIR / fname
        if path.exists():
            data[name] = pd.read_csv(path)
        else:
            logger.warning(f"[report] {fname} not found, skipping.")
    return data


def rupees(value: float) -> str:
    return f"Rs. {value:,.2f}"


def patient_summary(df):
    return {
        "total_patients": len(df),
        "avg_age":        round(df["age"].mean(), 1),
        "gender_dist":    df["gender"].value_counts().to_dict(),
        "insured_count":  int((df["insurance"].str.upper() == "YES").sum()),
        "ipd_count":      int((df["patient_type"].str.upper() == "IPD").sum()),
        "opd_count":      int((df["patient_type"].str.upper() == "OPD").sum()),
    }


def appointment_summary(df):
    status    = df["status"].value_counts().to_dict()
    total     = len(df)
    completed = status.get("Completed", 0)
    return {
        "total_appointments": total,
        "status_breakdown":   status,
        "completion_rate":    round(completed / total * 100, 1) if total else 0,
        "top_departments":    df["department_name"].value_counts().head(5).to_dict(),
        "visit_types":        df["visit_type"].value_counts().to_dict(),
    }


def billing_summary(df):
    return {
        "total_revenue":  df["total_amount"].sum(),
        "paid_amount":    df[df["payment_status"].str.lower() == "paid"]["total_amount"].sum(),
        "pending_amount": df[df["payment_status"].str.lower() != "paid"]["total_amount"].sum(),
        "avg_bill":       round(df["total_amount"].mean(), 2),
        "payment_modes":  df["payment_mode"].value_counts().to_dict(),
        "payment_status": df["payment_status"].value_counts().to_dict(),
        "total_discount": df["discount"].sum(),
    }


def admission_summary(df):
    return {
        "total_admissions": len(df),
        "avg_stay_days":    round(df["length_of_stay"].mean(), 1),
        "ward_types":       df["ward_type"].value_counts().to_dict(),
        "discharge_status": df["discharge_status"].value_counts().to_dict(),
    }


def lab_summary(df):
    return {
        "total_tests":   len(df),
        "status_dist":   df["status"].value_counts().to_dict(),
        "top_tests":     df["test_name"].value_counts().head(5).to_dict() if "test_name" in df.columns else {},
        "total_lab_rev": round(df["fee"].sum(), 2),
    }


def doctor_summary(df):
    return {
        "total_doctors":   len(df),
        "avg_experience":  round(df["experience_yrs"].mean(), 1),
        "avg_consult_fee": round(df["consultation_fee"].mean(), 2),
    }


def build_text_report(stats: dict, report_date: str) -> str:
    p  = stats.get("patients", {})
    a  = stats.get("appointments", {})
    b  = stats.get("billing", {})
    ad = stats.get("admissions", {})
    lb = stats.get("lab", {})
    dr = stats.get("doctors", {})

    lines = [
        "=" * 65,
        "      HOSPITAL ANALYTICS PIPELINE — SUMMARY REPORT",
        f"      Generated : {report_date}",
        "=" * 65,
        "", "1. PATIENT STATISTICS", "-" * 40,
        f"  Total patients       : {p.get('total_patients', 'N/A')}",
        f"  Average age          : {p.get('avg_age', 'N/A')} yrs",
        f"  Insured patients     : {p.get('insured_count', 'N/A')}",
        f"  OPD / IPD            : {p.get('opd_count','N/A')} / {p.get('ipd_count','N/A')}",
        "  Gender distribution  :",
    ]
    for g, c in p.get("gender_dist", {}).items():
        lines.append(f"      {g:<12}: {c}")

    lines += ["", "2. APPOINTMENTS", "-" * 40,
        f"  Total                : {a.get('total_appointments', 'N/A')}",
        f"  Completion rate      : {a.get('completion_rate', 'N/A')}%",
        "  Status breakdown     :"]
    for s, c in a.get("status_breakdown", {}).items():
        lines.append(f"      {s:<20}: {c}")
    lines.append("  Top departments      :")
    for d, c in a.get("top_departments", {}).items():
        lines.append(f"      {d:<30}: {c}")

    lines += ["", "3. BILLING & REVENUE", "-" * 40,
        f"  Total revenue        : {rupees(b.get('total_revenue', 0))}",
        f"  Paid                 : {rupees(b.get('paid_amount', 0))}",
        f"  Pending              : {rupees(b.get('pending_amount', 0))}",
        f"  Avg bill             : {rupees(b.get('avg_bill', 0))}",
        f"  Total discounts      : {rupees(b.get('total_discount', 0))}",
        "  Payment modes        :"]
    for m, c in b.get("payment_modes", {}).items():
        lines.append(f"      {m:<20}: {c}")

    lines += ["", "4. ADMISSIONS", "-" * 40,
        f"  Total                : {ad.get('total_admissions', 'N/A')}",
        f"  Avg stay             : {ad.get('avg_stay_days', 'N/A')} days",
        "  Ward types           :"]
    for w, c in ad.get("ward_types", {}).items():
        lines.append(f"      {w:<20}: {c}")

    lines += ["", "5. LAB TESTS", "-" * 40,
        f"  Total tests          : {lb.get('total_tests', 'N/A')}",
        f"  Lab revenue          : {rupees(lb.get('total_lab_rev', 0))}",
        "  Status distribution  :"]
    for s, c in lb.get("status_dist", {}).items():
        lines.append(f"      {s:<20}: {c}")

    lines += ["", "6. DOCTORS", "-" * 40,
        f"  Total doctors        : {dr.get('total_doctors', 'N/A')}",
        f"  Avg experience       : {dr.get('avg_experience', 'N/A')} yrs",
        f"  Avg consult fee      : {rupees(dr.get('avg_consult_fee', 0))}",
        "", "=" * 65, "  END OF REPORT", "=" * 65]

    return "\n".join(lines)


def generate_report() -> None:
    logger.info("Report generation started.")
    REPORT_DIR.mkdir(exist_ok=True)

    data        = load_cleaned()
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_slug   = datetime.now().strftime("%Y-%m-%d")

    stats = {}
    if "patients"     in data: stats["patients"]     = patient_summary(data["patients"])
    if "appointments" in data: stats["appointments"] = appointment_summary(data["appointments"])
    if "billing"      in data: stats["billing"]      = billing_summary(data["billing"])
    if "admission"    in data: stats["admissions"]   = admission_summary(data["admission"])
    if "labTests"     in data: stats["lab"]          = lab_summary(data["labTests"])
    if "doctors"      in data: stats["doctors"]      = doctor_summary(data["doctors"])

    txt_path = REPORT_DIR / f"hospital_report_{date_slug}.txt"
    txt_path.write_text(build_text_report(stats, report_date), encoding="utf-8")

    logger.info(f"Report saved → {txt_path}")
    logger.info("Report generation completed.")