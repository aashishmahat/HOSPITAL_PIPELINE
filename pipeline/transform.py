import pandas as pd
import numpy as np

def clean_patients(df):
    print("\n  cleaning patients...")
    df = df.copy()
    print(df.isnull().sum())
    df = df.drop_duplicates(subset=["patient_id"])
    df["gender"] = df["gender"].astype(str).str.strip().str.upper()
    df["gender"] = df["gender"].replace({
        "M": "Male",
        "F": "Female",
        "UN": "Unknown"
    })
    df['phone']=df['phone'].fillna("9800000000")
    df["gender"] = df["gender"].str.capitalize()
    print(df['gender'].unique())
    df["gender"]=df["gender"].replace({"Male":"M","Female":"F","Unknown":"un"})
    # df["gender"] = df["gender"].replace({"M": "Male","M":"male","M":"M","F": "Female","F":"female","F":"F","Un":"unknown"})
    df["age"] = df["age"].fillna(df["age"].median())
    df["blood_group"] = df["blood_group"].fillna("Unknown")
    df["address"]= df["address"].fillna("Not Provided")
    df["district"] = df["district"].fillna("Unknown")
    df["emergency_contact"] = df["emergency_contact"].fillna("Not Provided")
    print(df.isnull().sum())
    print(df.head())
    return df

def clean_doctors(df):
    print("\n cleaning doctors...")
    print(df.info())
    df=df.copy()
    df = df.drop_duplicates(subset=["doctor_id"])
    df["experience_yrs"]  = pd.to_numeric(df["experience_yrs"], errors="coerce")
    df["consultation_fee"] = pd.to_numeric(df["consultation_fee"], errors="coerce")
    df.loc[df["experience_yrs"] < 0,   "experience_yrs"]  = np.nan
    df.loc[df["consultation_fee"] <= 0, "consultation_fee"] = np.nan
    df["experience_yrs"]   = df["experience_yrs"].fillna(df["experience_yrs"].median())
    df["consultation_fee"] = df["consultation_fee"].fillna(df["consultation_fee"].median())
    df["qualification"] = df["qualification"].fillna("Not Specified")
    df["opd_timing"]    = df["opd_timing"].fillna("Not Specified")
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── department ────────────────────────────────────────────────────────────────
def clean_department(df):
    print("\n  cleaning department...")
    df=df.copy()
    df = df.drop_duplicates(subset=["department_id"])
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── admission ─────────────────────────────────────────────────────────────────
def clean_admission(df):
    print("\n  cleaning admission...")
    df=df.copy()
    df = df.drop_duplicates(subset=["admission_id"])
    df["length_of_stay"]   = pd.to_numeric(df["length_of_stay"],   errors="coerce")
    df["ward_fee_per_day"] = pd.to_numeric(df["ward_fee_per_day"], errors="coerce")
    df.loc[df["length_of_stay"]   < 0, "length_of_stay"]   = np.nan
    df.loc[df["ward_fee_per_day"] < 0, "ward_fee_per_day"] = np.nan
    df["length_of_stay"]   = df["length_of_stay"].fillna(df["length_of_stay"].median())
    df["ward_fee_per_day"] = df["ward_fee_per_day"].fillna(df["ward_fee_per_day"].median())
    df["discharge_date"]   = df["discharge_date"].fillna("Not Discharged")
    df["discharge_status"] = df["discharge_status"].fillna("Unknown")
    df["ward_type"]        = df["ward_type"].fillna("General")
    df["bed_number"]       = df["bed_number"].fillna("Unassigned")
    df["admission_date"]   = pd.to_datetime(df["admission_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── appointments ──────────────────────────────────────────────────────────────
def clean_appointments(df):
    print("\n  cleaning appointments...")
    df=df.copy()
    df = df.drop_duplicates(subset=["appointment_id"])
    df["consultation_fee"] = pd.to_numeric(df["consultation_fee"], errors="coerce")
    df.loc[df["consultation_fee"] < 0, "consultation_fee"] = np.nan
    df["consultation_fee"] = df["consultation_fee"].fillna(df["consultation_fee"].median())
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()
    df["status"] = df["status"].replace({"Done": "Completed", "Cancel": "Cancelled", "N/a": "Unknown"})
    df["doctor_name"]      = df["doctor_name"].fillna("Unknown")
    df["department_name"]  = df["department_name"].fillna("Unknown")
    df["appointment_time"] = df["appointment_time"].fillna("Not Recorded")
    df["notes"]            = df["notes"].fillna("None")
    df["appointment_date"] = pd.to_datetime(df["appointment_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── billing ───────────────────────────────────────────────────────────────────
def clean_billing(df):
    print("\n  cleaning billing...")
    df=df.copy()
    df = df.drop_duplicates(subset=["bill_id"])
    money_cols = ["consultation_fee", "lab_fee", "medicine_fee",
                  "ward_fee", "procedure_fee", "subtotal", "total_amount"]
    for col in money_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan
        df[col] = df[col].fillna(0)
    
    df['appointment_id']=df['appointment_id'].fillna("Not Mentioned")
    df['admission_id']=df['admission_id'].fillna("Not Mentioned")
    df["discount"]        = pd.to_numeric(df["discount"], errors="coerce").fillna(0)
    df["payment_mode"]    = df["payment_mode"].fillna("Unknown")
    df["payment_status"]  = df["payment_status"].fillna("Unknown")
    df["bill_date"]       = pd.to_datetime(df["bill_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── labTests ──────────────────────────────────────────────────────────────────
def clean_labTests(df):
    print("\n  cleaning labTests...")
    df=df.copy()
    df = df.drop_duplicates(subset=["lab_id"])
    df["fee"] = pd.to_numeric(df["fee"], errors="coerce")
    df.loc[df["fee"] < 0, "fee"] = np.nan
    df["fee"] = df["fee"].fillna(df["fee"].median())
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()
    df["status"] = df["status"].replace({"Done": "Completed", "N/a": "Unknown"})
    df["result"]          = df["result"].fillna("Pending")
    df["result_date"]     = df["result_date"].fillna("Not Available")
    df["reference_range"] = df["reference_range"].fillna("Not Specified")
    df["lab_technician"]  = df["lab_technician"].fillna("Unassigned")
    df["test_date"]       = pd.to_datetime(df["test_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df

 
# ── diagnoses ─────────────────────────────────────────────────────────────────
def clean_diagnoses(df):
    print("\n  cleaning diagnoses...")
    df=df.copy()
    df = df.drop_duplicates(subset=["diagnosis_id"])
    df["severity"] = df["severity"].astype(str).str.strip().str.capitalize()
    df["severity"] = df["severity"].replace({"N/a": "Unknown"})
    df["icd_code"] = df["icd_code"].fillna("Not Coded")
    df["follow_up_date"] = df["follow_up_date"].fillna("Not Scheduled")
    df["severity"] = df["severity"].fillna("Unknown")
    df["chronic"]= df["chronic"].fillna("Unknown")
    df["diagnosis_date"] = pd.to_datetime(df["diagnosis_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df
 
 
# ── prescription ──────────────────────────────────────────────────────────────
def clean_prescription(df):
    print("\n  cleaning prescription...")
    df=df.copy()
    print(df.head())
    df = df.drop_duplicates(subset=["prescription_id"])
    for col in ["quantity", "unit_price", "total_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan
        df[col] = df[col].fillna(df[col].median())
    df["dosage"]          = df["dosage"].fillna("As needed")
    df["duration"]        = df["duration"].fillna("Not Specified")
    df["dispensed"]       = df["dispensed"].fillna("No")
    df["form"]            = df["form"].fillna("Not Specified")
    df["prescribed_date"] = pd.to_datetime(df["prescribed_date"], errors="coerce")
    print(df.isnull().sum())
    print(df.head())
    return df
 
def transforms_data(datasets):
    print("Transform Starting data cleaning...")
    patients=datasets["patients"]
    doctors=datasets["doctors"]
    appointments=datasets['appointments']
    billing=datasets['billing']
    admission=datasets["admission"]
    department=datasets["department"]
    labTests=datasets["labTests"]
    diagnoses=datasets["diagnoses"]
    prescription=datasets["prescription"]
    # print("hello just testing !")
    # for name,df in datasets.items():
    #     print(f"{name} Dataset info")
    #     print(df.info())
    #     print(f"{name} Dataset shape")
    #     print(df.shape)
    #     print(f"{name} Dataset missing values:")
    #     print(df.isnull().sum())
    cleaned_data = {
        "patients":     clean_patients(patients),
        "doctors":      clean_doctors(doctors),
        "department":   clean_department(department),
        "admission":    clean_admission(admission),
        "appointments": clean_appointments(appointments),
        "billing":      clean_billing(billing),
        "labTests":     clean_labTests(labTests),
        "diagnoses":    clean_diagnoses(diagnoses),
        "prescription": clean_prescription(prescription),
    }
    print("\nTransform: All datasets cleaned successfully.")
    return cleaned_data