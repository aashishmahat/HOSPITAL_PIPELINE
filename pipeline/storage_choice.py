import numpy as np
import pandas as pd
import sqlite3
from pprint import pprint

def Storage_Choice(cleaned_data):
    pprint("let's choose for the storage as your choice.")
    conn=sqlite3.connect("hospital.db")
    cursor=conn.cursor()
    for name,df in cleaned_data.items():
        pprint(f"Inserting into table:{name}")
        df.to_sql(name,conn,if_exists="replace",index=False)
    pprint("All data inserted successfully!")
    patients_name=input("Enter the patient id:")
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?",(f"%{patients_name}%",))
    rows=cursor.fetchall()
    if rows:
        pprint(rows)
    
    else:
        pprint(f"No patient found with ID {patients_name}")
    conn.close()