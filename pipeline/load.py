import os
from pprint import pprint

def save_to_csv(cleaned_data, folder_name="cleaned_data"):
    pprint("Saving data to CSV files...")

    # Create folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    for name, df in cleaned_data.items():
        file_path = os.path.join(folder_name, f"{name}_cleaned.csv")
        df.to_csv(file_path, index=False)
        pprint(f"Saved: {file_path}")

    pprint("All CSV files saved successfully!")