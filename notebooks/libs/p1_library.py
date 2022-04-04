import pandas as pd
from pathlib import Path
import numpy as np
import os

def chemical_filter(file_path, chemical_list):
    chemical_data = []

    for filename in os.listdir(file_path):
        if filename.endswith(".csv"):
            csv_data = pd.read_csv(file_path +'/'+ filename, parse_dates=True, infer_datetime_format=True)
            for item in chemical_list:
                chemicals_filtered = csv_data[csv_data['CHEMICAL_NAME'] == item]
                chemicals_filtered = chemicals_filtered.iloc[: , 1:]
                chemical_data.append(chemicals_filtered)

    return pd.concat(chemical_data)
