import pandas as pd

def patient_report(cleaned_data, filename="report/text_report/patient_report.txt"):
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


def doctor_patient(cleaned_data, filename="report/text_report/doctor_patient.txt"):
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


def lab_summary(cleaned_data, filename="report/text_report/lab_summary.txt"):
    df = cleaned_data.get("labTests")

    if df is None or df.empty:
        return {
            "total_tests": 0,
            "status_dist": {},
            "top_tests": {},
            "total_lab_rev": 0.0,
        }

    summary = {
        "total_tests":   len(df),
        "status_dist":   df["status"].value_counts().to_dict()           if "status"    in df.columns else {},
        "top_tests":     df["test_name"].value_counts().head(5).to_dict() if "test_name" in df.columns else {},
        "total_lab_rev": round(df["fee"].sum(), 2)                        if "fee"       in df.columns else 0.0,
    }

    with open(filename, "w") as f:
        f.write("=== LAB SUMMARY REPORT ===\n\n")

        f.write(f"Total Tests: {summary['total_tests']}\n")
        f.write(f"Total Lab Revenue: {summary['total_lab_rev']}\n")

        f.write("\nTest Status Distribution:\n")
        if summary["status_dist"]:
            status_series = pd.Series(summary["status_dist"])
            f.write(status_series.to_string())
            f.write("\n")

        f.write("\nTop 5 Tests Ordered:\n")
        if summary["top_tests"]:
            top_series = pd.Series(summary["top_tests"])
            f.write(top_series.to_string())
            f.write("\n")

    return summary


def billing_summary(cleaned_data, filename="report/text_report/billing_summary.txt"):
    df = cleaned_data.get("billing")

    if df is None or df.empty:
        return {
            "total_revenue":  0.0,
            "paid_amount":    0.0,
            "pending_amount": 0.0,
            "avg_bill":       0.0,
            "payment_modes":  {},
            "payment_status": {},
            "total_discount": 0.0,
        }

    summary = {
        "total_revenue":  df["total_amount"].sum()
                          if "total_amount" in df.columns else 0.0,
        "paid_amount":    df[df["payment_status"].str.lower() == "paid"]["total_amount"].sum()
                          if "payment_status" in df.columns and "total_amount" in df.columns else 0.0,
        "pending_amount": df[df["payment_status"].str.lower() != "paid"]["total_amount"].sum()
                          if "payment_status" in df.columns and "total_amount" in df.columns else 0.0,
        "avg_bill":       round(df["total_amount"].mean(), 2)
                          if "total_amount" in df.columns else 0.0,
        "payment_modes":  df["payment_mode"].value_counts().to_dict()
                          if "payment_mode" in df.columns else {},
        "payment_status": df["payment_status"].value_counts().to_dict()
                          if "payment_status" in df.columns else {},
        "total_discount": df["discount"].sum()
                          if "discount" in df.columns else 0.0,
    }

    with open(filename, "w") as f:
        f.write("=== BILLING SUMMARY REPORT ===\n\n")

        f.write(f"Total Revenue: {summary['total_revenue']}\n")
        f.write(f"Paid Amount: {summary['paid_amount']}\n")
        f.write(f"Pending Amount: {summary['pending_amount']}\n")
        f.write(f"Average Bill: {summary['avg_bill']}\n")
        f.write(f"Total Discounts: {summary['total_discount']}\n")

        f.write("\nPayment Status Distribution:\n")
        if summary["payment_status"]:
            f.write(pd.Series(summary["payment_status"]).to_string())
            f.write("\n")

        f.write("\nPayment Mode Distribution:\n")
        if summary["payment_modes"]:
            f.write(pd.Series(summary["payment_modes"]).to_string())
            f.write("\n")

    return summary




def admission_report(cleaned_data, filename="report/text_report/admission_report.txt"):
    df = cleaned_data.get("admission")

    if df is None or df.empty:
        with open(filename, "w") as f:
            f.write("=== ADMISSION REPORT ===\n\nNo data available.\n")
        return {}

    with open(filename, "w") as f:
        f.write("=== ADMISSION REPORT ===\n\n")

        f.write(f"Total Admissions: {len(df)}\n")

        if "length_of_stay" in df.columns:
            f.write(f"Average Length of Stay: {round(df['length_of_stay'].mean(), 2)} days\n")
            f.write(f"Max Length of Stay: {df['length_of_stay'].max()} days\n")
            f.write(f"Min Length of Stay: {df['length_of_stay'].min()} days\n")

        if "ward_type" in df.columns:
            f.write("\nWard Type Distribution:\n")
            f.write(df["ward_type"].value_counts().to_string())
            f.write("\n")

        if "discharge_status" in df.columns:
            f.write("\nDischarge Status Distribution:\n")
            f.write(df["discharge_status"].value_counts().to_string())
            f.write("\n")

        if "total_ward_charges" in df.columns:
            f.write(f"\nTotal Ward Charges: {df['total_ward_charges'].sum()}\n")
            f.write(f"Average Ward Charges: {round(df['total_ward_charges'].mean(), 2)}\n")

    return df


def diagnosis_report(cleaned_data, filename="report/text_report/diagnosis_report.txt"):
    df = cleaned_data.get("diagnoses")

    if df is None or df.empty:
        with open(filename, "w") as f:
            f.write("=== DIAGNOSIS REPORT ===\n\nNo data available.\n")
        return {}

    with open(filename, "w") as f:
        f.write("=== DIAGNOSIS REPORT ===\n\n")

        f.write(f"Total Diagnosis Records: {len(df)}\n")

        if "diagnosis" in df.columns:
            f.write("\nTop 10 Diagnoses:\n")
            f.write(df["diagnosis"].value_counts().head(10).to_string())
            f.write("\n")

        if "severity" in df.columns:
            f.write("\nSeverity Distribution:\n")
            f.write(df["severity"].value_counts().to_string())
            f.write("\n")

        if "diagnosis_date" in df.columns:
            df["diagnosis_date"] = pd.to_datetime(df["diagnosis_date"], errors="coerce")
            f.write(f"\nEarliest Diagnosis Date: {df['diagnosis_date'].min().date()}\n")
            f.write(f"Latest Diagnosis Date: {df['diagnosis_date'].max().date()}\n")

    return df


def prescription_report(cleaned_data, filename="report/text_report/prescription_report.txt"):
    df = cleaned_data.get("prescription")

    if df is None or df.empty:
        with open(filename, "w") as f:
            f.write("=== PRESCRIPTION REPORT ===\n\nNo data available.\n")
        return {}

    with open(filename, "w") as f:
        f.write("=== PRESCRIPTION REPORT ===\n\n")

        f.write(f"Total Prescriptions: {len(df)}\n")

        if "medicine_name" in df.columns:
            f.write("\nTop 10 Medicines Prescribed:\n")
            f.write(df["medicine_name"].value_counts().head(10).to_string())
            f.write("\n")

        if "dosage" in df.columns:
            f.write("\nDosage Distribution:\n")
            f.write(df["dosage"].value_counts().to_string())
            f.write("\n")

        if "duration_days" in df.columns:
            f.write(f"\nAverage Prescription Duration: {round(df['duration_days'].mean(), 2)} days\n")
            f.write(f"Max Prescription Duration: {df['duration_days'].max()} days\n")

        if "doctor_id" in df.columns:
            f.write(f"\nUnique Doctors Prescribing: {df['doctor_id'].nunique()}\n")

        if "patient_id" in df.columns:
            f.write(f"Unique Patients with Prescriptions: {df['patient_id'].nunique()}\n")

    return df


def appointment_report(cleaned_data, filename="report/text_report/appointment_report.txt"):
    df = cleaned_data.get("appointments")

    if df is None or df.empty:
        with open(filename, "w") as f:
            f.write("=== APPOINTMENT REPORT ===\n\nNo data available.\n")
        return {}

    with open(filename, "w") as f:
        f.write("=== APPOINTMENT REPORT ===\n\n")

        f.write(f"Total Appointments: {len(df)}\n")

        if "status" in df.columns:
            total = len(df)
            completed = (df["status"] == "Completed").sum()
            f.write(f"Completed Appointments: {completed}\n")
            f.write(f"Completion Rate: {round(completed / total * 100, 2)}%\n")

            f.write("\nAppointment Status Distribution:\n")
            f.write(df["status"].value_counts().to_string())
            f.write("\n")

        if "department_name" in df.columns:
            f.write("\nTop 10 Departments by Appointments:\n")
            f.write(df["department_name"].value_counts().head(10).to_string())
            f.write("\n")

        if "visit_type" in df.columns:
            f.write("\nVisit Type Distribution:\n")
            f.write(df["visit_type"].value_counts().to_string())
            f.write("\n")

        if "appointment_date" in df.columns:
            df["appointment_date"] = pd.to_datetime(df["appointment_date"], errors="coerce")
            f.write(f"\nEarliest Appointment: {df['appointment_date'].min().date()}\n")
            f.write(f"Latest Appointment: {df['appointment_date'].max().date()}\n")

    return df


def doctor_report(cleaned_data, filename="report/text_report/doctor_report.txt"):
    df = cleaned_data.get("doctors")

    if df is None or df.empty:
        with open(filename, "w") as f:
            f.write("=== DOCTOR REPORT ===\n\nNo data available.\n")
        return {}

    with open(filename, "w") as f:
        f.write("=== DOCTOR REPORT ===\n\n")

        f.write(f"Total Doctors: {len(df)}\n")

        if "experience_yrs" in df.columns:
            f.write(f"Average Experience: {round(df['experience_yrs'].mean(), 2)} years\n")
            f.write(f"Most Experienced: {df['experience_yrs'].max()} years\n")

        if "consultation_fee" in df.columns:
            f.write(f"Average Consultation Fee: {round(df['consultation_fee'].mean(), 2)}\n")
            f.write(f"Highest Consultation Fee: {df['consultation_fee'].max()}\n")

        spec_col = next((c for c in ["specialty", "specialization", "department_name"]
                         if c in df.columns), None)
        if spec_col:
            f.write(f"\nSpecialty Distribution:\n")
            f.write(df[spec_col].value_counts().to_string())
            f.write("\n")

        if "gender" in df.columns:
            f.write("\nDoctor Gender Distribution:\n")
            f.write(df["gender"].value_counts().to_string())
            f.write("\n")

    return df




def generate_all_reports(cleaned_data):
    """Run all report generation functions at once."""
    import os
    os.makedirs("report", exist_ok=True)

    patient_report(cleaned_data)
    doctor_patient(cleaned_data)
    lab_summary(cleaned_data)
    billing_summary(cleaned_data)
    admission_report(cleaned_data)
    diagnosis_report(cleaned_data)
    prescription_report(cleaned_data)
    appointment_report(cleaned_data)
    doctor_report(cleaned_data)

    print("All reports generated successfully in the /report folder.")