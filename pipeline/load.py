from pathlib import Path    
import os
LOAD_DATA=Path("cleaned_data")

def store(cleaned_data):
    for name ,df in cleaned_data.items():
        os.makedirs(LOAD_DATA,exist_ok=True)
        file_path=os.path.join(LOAD_DATA,f"{name}_cleaned.csv")
        df.to_csv(file_path,index=False)
    print("Data stored successfully!")
    
