import pandas as pd
from pathlib import Path
DATA_FOLDER=Path("data_dirty")
FILES={
    "admission":"admissions_dirty.csv",
    "doctors":"doctors_dirty.csv",
    "appointments":"appointments_dirty.csv",
    "billing":"billing_dirty.csv",
    "department":"departments_dirty.csv",
    "labTests":'lab_tests_dirty.csv',
    "diagnoses":"diagnoses_dirty.csv",
    "patients":"patients_dirty.csv",
    "prescription":"prescriptions_dirty.csv"
}

def load_datasets():
    datasets = {}

    for name, file in FILES.items():
        file_path = DATA_FOLDER / file
        try:
            datasets[name] = pd.read_csv(file_path)
            rows,column=datasets[name].shape
            print(f"{name} loaded-{rows} rows X {column} columns")
        except FileNotFoundError:
            print(f"Error: {file} not found")  
    print(f"\n Total datasets loaded:{len(datasets)}")
    return datasets

# ld=load_datasets()
# # print(ld['patients'].head())
# for name,df in ld.items():
#     print(f"{name} KO DATA HERDAI")
#     print(df.head())

 