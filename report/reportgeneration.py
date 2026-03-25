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
