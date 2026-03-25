import pandas as pd
import numpy as np

# ── Helper: Cap outliers using IQR ─────────────────────────────────────────────
def remove_outliers_iqr(df, col):
    if col not in df.columns:
        return df
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = np.where(df[col] < lower, lower, df[col])
    df[col] = np.where(df[col] > upper, upper, df[col])
    return df


# ── Patients ───────────────────────────────────────────────────────────────────
def clean_patients(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["patient_id"])
    df["gender"] = df["gender"].astype(str).str.strip().str.upper()
    df["gender"] = df["gender"].replace({"M": "Male", "F": "Female", "UN": "Unknown"})
    df["gender"] = df["gender"].fillna("Unknown").str.capitalize()
    df["gender"] = df["gender"].replace({"Male":"M","Female":"F","Unknown":"UN"})
    df = remove_outliers_iqr(df, "age")
    df["age"] = df["age"].fillna(df["age"].median())
    
    df["blood_group"] = df["blood_group"].fillna("Unknown")
    df["phone"] = df["phone"].fillna("9800000000")
    df["address"] = df["address"].fillna("Not Provided")
    df["district"] = df["district"].fillna("Unknown")
    df["emergency_contact"] = df["emergency_contact"].fillna("Not Provided")
    
    return df


# ── Doctors ────────────────────────────────────────────────────────────────────
def clean_doctors(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["doctor_id"])
    
    df["experience_yrs"] = pd.to_numeric(df["experience_yrs"], errors="coerce")
    df["consultation_fee"] = pd.to_numeric(df["consultation_fee"], errors="coerce")
    
    df.loc[df["experience_yrs"] < 0, "experience_yrs"] = np.nan
    df.loc[df["consultation_fee"] <= 0, "consultation_fee"] = np.nan
    
    df["experience_yrs"] = df["experience_yrs"].fillna(df["experience_yrs"].median())
    df["consultation_fee"] = df["consultation_fee"].fillna(df["consultation_fee"].median())
    
    df = remove_outliers_iqr(df, "experience_yrs")
    df = remove_outliers_iqr(df, "consultation_fee")
    
    df["qualification"] = df["qualification"].fillna("Not Specified")
    df["opd_timing"] = df["opd_timing"].fillna("Not Specified")
    
    return df


# ── Department ────────────────────────────────────────────────────────────────
def clean_department(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["department_id"])
    return df


# ── Admission ─────────────────────────────────────────────────────────────────
def clean_admission(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["admission_id"])
    
    df["length_of_stay"] = pd.to_numeric(df["length_of_stay"], errors="coerce")
    df["ward_fee_per_day"] = pd.to_numeric(df["ward_fee_per_day"], errors="coerce")
    
    df.loc[df["length_of_stay"] < 0, "length_of_stay"] = np.nan
    df.loc[df["ward_fee_per_day"] < 0, "ward_fee_per_day"] = np.nan
    
    df["length_of_stay"] = df["length_of_stay"].fillna(df["length_of_stay"].median())
    df["ward_fee_per_day"] = df["ward_fee_per_day"].fillna(df["ward_fee_per_day"].median())
    
    df = remove_outliers_iqr(df, "length_of_stay")
    df = remove_outliers_iqr(df, "ward_fee_per_day")
    
    df["discharge_date"] = df["discharge_date"].fillna("Not Discharged")
    df["discharge_status"] = df["discharge_status"].fillna("Unknown")
    df["ward_type"] = df["ward_type"].fillna("General")
    df["bed_number"] = df["bed_number"].fillna("Unassigned")
    
    df["admission_date"] = pd.to_datetime(df["admission_date"], errors="coerce")
    
    return df


# ── Appointments ──────────────────────────────────────────────────────────────
def clean_appointments(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["appointment_id"])
    
    df["consultation_fee"] = pd.to_numeric(df["consultation_fee"], errors="coerce")
    df.loc[df["consultation_fee"] < 0, "consultation_fee"] = np.nan
    df["consultation_fee"] = df["consultation_fee"].fillna(df["consultation_fee"].median())
    df = remove_outliers_iqr(df, "consultation_fee")
    
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()
    df["status"] = df["status"].replace({"Done": "Completed", "Cancel": "Cancelled", "N/a": "Unknown"})
    
    df["doctor_name"] = df["doctor_name"].fillna("Unknown")
    df["department_name"] = df["department_name"].fillna("Unknown")
    df["appointment_time"] = df["appointment_time"].fillna("Not Recorded")
    df["notes"] = df["notes"].fillna("None")
    df["appointment_date"] = pd.to_datetime(df["appointment_date"], errors="coerce")
    
    return df


# ── Billing ───────────────────────────────────────────────────────────────────
def clean_billing(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["bill_id"])
    
    money_cols = ["consultation_fee", "lab_fee", "medicine_fee", "ward_fee",
                  "procedure_fee", "subtotal", "total_amount", "discount"]
    
    for col in money_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        df.loc[df[col] < 0, col] = 0
        df = remove_outliers_iqr(df, col)
    
    df["appointment_id"] = df["appointment_id"].fillna("Not Mentioned")
    df["admission_id"] = df["admission_id"].fillna("Not Mentioned")
    df["payment_mode"] = df["payment_mode"].fillna("Unknown")
    df["payment_status"] = df["payment_status"].fillna("Unknown")
    df["bill_date"] = pd.to_datetime(df["bill_date"], errors="coerce")
    
    return df


# ── Lab Tests ─────────────────────────────────────────────────────────────────
def clean_labTests(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["lab_id"])
    
    df["fee"] = pd.to_numeric(df["fee"], errors="coerce")
    df.loc[df["fee"] < 0, "fee"] = np.nan
    df["fee"] = df["fee"].fillna(df["fee"].median())
    df = remove_outliers_iqr(df, "fee")
    
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()
    df["status"] = df["status"].replace({"Done": "Completed", "N/a": "Unknown"})
    df["result"] = df["result"].fillna("Pending")
    df["result_date"] = df["result_date"].fillna("Not Available")
    df["reference_range"] = df["reference_range"].fillna("Not Specified")
    df["lab_technician"] = df["lab_technician"].fillna("Unassigned")
    df["test_date"] = pd.to_datetime(df["test_date"], errors="coerce")
    
    return df


# ── Diagnoses ─────────────────────────────────────────────────────────────────
def clean_diagnoses(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["diagnosis_id"])
    
    df["severity"] = df["severity"].astype(str).str.strip().str.capitalize()
    df["severity"] = df["severity"].replace({"N/a": "Unknown"}).fillna("Unknown")
    
    df["icd_code"] = df["icd_code"].fillna("Not Coded")
    df["follow_up_date"] = df["follow_up_date"].fillna("Not Scheduled")
    df["chronic"] = df["chronic"].fillna("Unknown")
    df["diagnosis_date"] = pd.to_datetime(df["diagnosis_date"], errors="coerce")
    
    return df


# ── Prescription ──────────────────────────────────────────────────────────────
def clean_prescription(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["prescription_id"])
    
    for col in ["quantity", "unit_price", "total_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan
        df[col] = df[col].fillna(df[col].median())
        df = remove_outliers_iqr(df, col)
    
    df["dosage"] = df["dosage"].fillna("As needed")
    df["duration"] = df["duration"].fillna("Not Specified")
    df["dispensed"] = df["dispensed"].fillna("No")
    df["form"] = df["form"].fillna("Not Specified")
    df["prescribed_date"] = pd.to_datetime(df["prescribed_date"], errors="coerce")
    
    return df


# ── Transform all datasets ─────────────────────────────────────────────────────
def transforms_data(datasets):
    cleaned_data = {
        "patients": clean_patients(datasets["patients"]),
        "doctors": clean_doctors(datasets["doctors"]),
        "department": clean_department(datasets["department"]),
        "admission": clean_admission(datasets["admission"]),
        "appointments": clean_appointments(datasets["appointments"]),
        "billing": clean_billing(datasets["billing"]),
        "labTests": clean_labTests(datasets["labTests"]),
        "diagnoses": clean_diagnoses(datasets["diagnoses"]),
        "prescription": clean_prescription(datasets["prescription"]),
    }
    return cleaned_data