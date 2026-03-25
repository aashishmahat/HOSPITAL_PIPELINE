import pandas as pd

def patient_report(cleaned_data, filename="report/patient_report.txt"):
    patient_admission = pd.merge(
        cleaned_data['patients'],
        cleaned_data['admission'],
        on='patient_id',
        how='left'
    )

    with open(filename, "w") as f:
        f.write("=== PATIENT REPORT ===\n\n")

        # Total patients
        f.write(f"Total Patients: {len(patient_admission)}\n")

        # Admitted vs Not Admitted
        admitted = patient_admission['ward_type'].notna().sum()
        not_admitted = patient_admission['ward_type'].isna().sum()
        f.write(f"Admitted Patients: {admitted}\n")
        f.write(f"Not Admitted Patients: {not_admitted}\n")

        # Gender distribution
        f.write("\nGender Distribution:\n")
        f.write(patient_admission['gender'].value_counts().to_string())
        f.write("\n")
        # Average age
        f.write(f"\nAverage Age: {patient_admission['age'].mean()}\n")

        # Ward type distribution
        f.write("\nWard Type Distribution:\n")
        f.write(patient_admission['ward_type'].value_counts().to_string())
        f.write("\n")

        # Total revenue
        f.write(f"\nTotal Ward Revenue: {patient_admission['total_ward_charges'].sum()}\n")

    return patient_admission

def doctor_patient(cleaned_data, filename="report/doctor_patient.txt"):
    # Merge appointments with doctors
    doc_app = pd.merge(
        cleaned_data['appointments'],
        cleaned_data['doctors'],
        on='doctor_id',
        how='left'
    )

    # Count number of patients per doctor
    patient_count = doc_app.groupby('doctor_name')['patient_id'].nunique()

    # Write to file
    with open(filename, "w") as f:
        f.write("=== DOCTOR - PATIENT REPORT ===\n\n")
        f.write("Number of Patients per Doctor:\n")
        f.write(patient_count.to_string())
        f.write("\n")

    return patient_count
def lab_summary(cleaned_data, filename="report/lab_summary.txt"):
    # Extract the labTests DataFrame from cleaned_data
    df = cleaned_data.get("labTests")
    
    if df is None or df.empty:
        return {
            "total_tests": 0,
            "status_dist": {},
            "top_tests": {},
            "total_lab_rev": 0.0,
        }

    summary = {
        "total_tests": len(df),
        "status_dist": df["status"].value_counts().to_dict() if "status" in df.columns else {},
        "top_tests": df["test_name"].value_counts().head(5).to_dict() if "test_name" in df.columns else {},
        "total_lab_rev": round(df["fee"].sum(), 2) if "fee" in df.columns else 0.0,
    }

    # Optional: write to file
    with open(filename, "w") as f:
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")

    return summary

def billing_summary(cleaned_data, filename="report/billing_summary.txt"):
    # Extract the billing DataFrame from cleaned_data
    df = cleaned_data.get("billing")
    
    if df is None or df.empty:
        return {
            "total_revenue": 0.0,
            "paid_amount": 0.0,
            "pending_amount": 0.0,
            "avg_bill": 0.0,
            "payment_modes": {},
            "payment_status": {},
            "total_discount": 0.0,
        }
    
    summary = {
        "total_revenue": df["total_amount"].sum() if "total_amount" in df.columns else 0.0,
        "paid_amount": df[df["payment_status"].str.lower() == "paid"]["total_amount"].sum()
                        if "payment_status" in df.columns and "total_amount" in df.columns else 0.0,
        "pending_amount": df[df["payment_status"].str.lower() != "paid"]["total_amount"].sum()
                        if "payment_status" in df.columns and "total_amount" in df.columns else 0.0,
        "avg_bill": round(df["total_amount"].mean(), 2) if "total_amount" in df.columns else 0.0,
        "payment_modes": df["payment_mode"].value_counts().to_dict() if "payment_mode" in df.columns else {},
        "payment_status": df["payment_status"].value_counts().to_dict() if "payment_status" in df.columns else {},
        "total_discount": df["discount"].sum() if "discount" in df.columns else 0.0,
    }

    # Optional: write summary to file
    with open(filename, "w") as f:
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")

    return summary

def generate_all_reports(cleaned_data):
    """Run all report generation functions at once."""
    import os
    os.makedirs("report", exist_ok=True)
    patient_report(cleaned_data)
    doctor_patient(cleaned_data)
    lab_summary(cleaned_data)
    billing_summary(cleaned_data)
    print("All reports generated successfully in the /report folder.")

