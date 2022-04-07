import pandas as pd
from pathlib import Path
import numpy as np
import os

###

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


###

def chemical_to_moles(df):

    molar_mass_dict={
            "2,3,7,8-Tetrachlorodibenzo-p-dioxin":321.97,
            "Cyanide":26.02,
            "Dieldrin":380.91,
            "Hexachlorobiphenyl; 3,3',4,4',5,5'- (PCB 169)":360.878,
            "Lead":207.2,
            "Mercury":200.59,
            "Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)":326.433
    }

    conversion_factor_dict={
            'pg/g':10**-6,
            'pg/sample':10**-6,
            'ppt':10**-6,
            'ppb':10**-3,
            'ppm':1,
            'ug/kg':10**-3,
            'UMOLES/G':1,
            'ng/g':10**-3,
            'umol/g':1,
            'mg/kg':1,
            'ng/kg':10**-6,
            'pg':10**-4,
            'pg/l':10**-9,
            'ng/l':10**-6,
            'ug/l':10**-3,
            'mg/l':1
    }
    df['REPORT_RESULT_UNIT'].fillna('ug/kg',inplace=True)
    df.dropna(subset=['REPORT_RESULT_VALUE'],inplace=True)
    df.isnull().sum()

    def unit_conversion(row):
        REPORT_RESULT_VALUE, REPORT_RESULT_UNIT = row.REPORT_RESULT_VALUE, row.REPORT_RESULT_UNIT
        conversion = conversion_factor_dict[REPORT_RESULT_UNIT]
    
        if REPORT_RESULT_UNIT == 'UMOLES/G' or REPORT_RESULT_UNIT == 'umol/g':
            return REPORT_RESULT_VALUE**2
        else:
            return REPORT_RESULT_VALUE*conversion


    df['VALUE_MUGRAM_PER_GRAM'] = df.apply(unit_conversion,axis=1)

    def value_moles(row):
            CHEMICAL_NAME, VALUE_MUGRAM_PER_GRAM = row.CHEMICAL_NAME, row.VALUE_MUGRAM_PER_GRAM
            molar = molar_mass_dict[CHEMICAL_NAME]

            return VALUE_MUGRAM_PER_GRAM / molar

    df['VALUE_MUMOL_PER_GRAM'] = df.apply(value_moles,axis=1)

    return df