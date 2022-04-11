import pandas as pd
from pathlib import Path
import numpy as np
import os
import panel as pn
pn.extension('plotly')
import plotly.express as px
import hvplot.pandas
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ipywidgets as widgets
import holoviews as hv
hv.extension('bokeh')
from ipywidgets import interact, interactive, fixed, interact_manual
from pathlib import Path
from dotenv import load_dotenv
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

######

# LISTS

# List of 8 Contaminants of Concern flagged by EPA as most dangerous
contaminant_list_8COCs = [
    # Metals
    "Copper",
    "Lead", 
    "Mercury", 
    # Dioxin (example compound - worst in dioxin class)
    "2,3,7,8-Tetrachlorodibenzo-p-dioxin",  
    # Dieldrin
    "Dieldrin",
    # DDT (example compound - most recognizable name in DDT class)
    "p,p'-DDT",
    # PAHs (example compound - worst in PAH class)
    "Benzo(a)pyrene",
    # PCBs (example compound - among the worst in PCB class)
    "Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)"
]

# List of the nicknames for the 8 COCs, as used in variables (not inside dataframes)
coc_variable_list = [
    "copper",
    "lead",
    "mercury",
    "dioxin",
    "dieldrin",
    "DDT",
    "pah",
    "pcb"
]

# List of 30 top contaminants (including 8 COCs)
contaminant_list_30 = [
    '2,3,7,8-Tetrachlorodibenzo-p-dioxin',
    'Cyanide',
    'Dieldrin',
    "Hexachlorobiphenyl; 3,3',4,4',5,5'- (PCB 169)",
    'Lead',
    'Mercury',
    'Copper',
    'Benzo(a)pyrene',
    "Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)",
    '1,2-Dichlorobenzene',
    '1,4-Dichlorobenzene',
    '2-Chlorophenol',
    'Chlorobenzene',
    "p,p'-DDD",
    'Benzene',
    'Chloroform',
    "Pentachlorobiphenyl; 2',3,4,4',5- (PCB 123)",
    "p,p'-DDT",
    "p,p'-DDE",
    'Aldrin',
    'Aroclor 1016',
    'Aroclor 1221',
    'Aroclor 1232',
    'Aroclor 1242',
    'Aroclor 1248',
    'Aroclor 1254',
    'Aroclor 1260',
    "Pentachlorobiphenyl; 2,3,3',4,4'- (PCB 105)",
    "Pentachlorobiphenyl; 2,3,3',4',6- (PCB 110)",
    "Pentachlorobiphenyl; 2,3,4,4',5- (PCB 114)",
    "Pentachlorobiphenyl; 2,3',4,4',5- (PCB 118)",
    'Chromium'
]

# List of industry categories in industry dataframe
industry_list = [
    'copper',
    'lead',
    'mercury',
    'dioxins',
    'dieldrin',
    'DDT',
    'PAHs',
    'PCBs'
]

######

# DICTIONARIES

# 8 COC Dictionary matches the coc name used in all variables 
# to the official chemical name used inside all sampling dataframes.
eight_coc_dict = {
   # Metals
    "copper":"Copper",
    "lead":"Lead",
    "mercury":"Mercury",
    # Dioxin (example compound - worst in dioxin class)
    "dioxin":"2,3,7,8-Tetrachlorodibenzo-p-dioxin",
    # Dieldrin
    "dieldrin":"Dieldrin",
    # DDT (example compound - most recognizable name in DDT class)
    "DDT":"p,p'-DDT",
    # PAHs (example compound - worst in PAH class)
    "pah":"Benzo(a)pyrene",
    # PCBs (example compound - among the worst in PCB class)
    "pcb":"Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)"
}

# Molar Mass Dictionary matches top each of the 30 compounds (including 8 COCs) to its molar mass.
molar_mass_dict={
        "2,3,7,8-Tetrachlorodibenzo-p-dioxin":321.97,
        "Cyanide":26.02,
        "Dieldrin":380.91,
        "Hexachlorobiphenyl; 3,3',4,4',5,5'- (PCB 169)":360.878,
        "Lead":207.20,
        "Mercury":200.59,
        "Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)":326.433,
        "1,2-Dichlorobenzene":147.01,
        "1,4-Dichlorobenzene":147.00,
        "2-Chlorophenol":128.56,
        "Chlorobenzene":112.56,
        "p,p'-DDD":320.00,
        "Benzene":78.11,
        "Chloroform":119.38,
        "Pentachlorobiphenyl; 2',3,4,4',5- (PCB 123)":326.40,
        "p,p'-DDT":354.50,
        "p,p'-DDE":318.02,
        "Aldrin":364.90,
        "Aroclor 1016":257.543,
        "Aroclor 1221":188.653,
        "Aroclor 1232":188.653,
        "Aroclor 1242":260.57,
        "Aroclor 1248":291.988,
        "Aroclor 1254":326.40,
        "Aroclor 1260":376,
        "Pentachlorobiphenyl; 2,3,3',4,4'- (PCB 105)":326.40,
        "Pentachlorobiphenyl; 2,3,3',4',6- (PCB 110)":326.40,
        "Pentachlorobiphenyl; 2,3,4,4',5- (PCB 114)":326.40,
        "Pentachlorobiphenyl; 2,3',4,4',5- (PCB 118)":323.883,
        "Chromium":51.996,
        "Benzo(a)pyrene":252.31,
        "Copper":63.546
    }

# Conversion Factor Dictionary matches each type of sampling unit to its amount in microgram/gram (ug/g)
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
            'pg':10**-6,
            'pg/l':10**-9,
            'ng/l':10**-6,
            'ug/l':10**-3,
            'mg/l':1,
            'ng/ml':10**-3
        }

######

# FUNCTIONS

# All Clean Data Function - returns a dataframe.
# This function spins through the filepath containing all clean data 
# csvs and creates a dataframe of all information. 
# WARNING: resulting dataframe is almost 4 million rows.
def clean_data_df(file_path):
    clean_data = []

    for filename in os.listdir(file_path):
        if filename.endswith(".csv"):
            csv_data = pd.read_csv(file_path + '/' + filename, parse_dates=True, infer_datetime_format=True)
            clean_data.append(csv_data)

    return pd.concat(clean_data)

# Chemical Filter Function - returns a dataframe.
# This function spins through the filepath containing all clean data 
# csvs and creates a dataframe of only the specified chemicals.
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


# Convert Sampling Units to Moles function - returns a dataframe.
# This function ingests a dataframe, reads the sample values and add columns
# with the converted value to ug/g and umol/g.
def chemical_to_moles(df):

    units_to_convert = list(conversion_factor_dict.keys())
    
    df.dropna(subset=['REPORT_RESULT_VALUE','REPORT_RESULT_UNIT'],inplace=True)
    df = df[df['REPORT_RESULT_UNIT'].isin(units_to_convert)]

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


# Convert Sampling Units to ug/g function - returns a dataframe.
# This function ingests a dataframe, reads the sample values and adds
# one column with the value converted to ug/g.
def chemical_to_ugrams(df):

    units_to_convert = list(conversion_factor_dict.keys())
    
    df.dropna(subset=['REPORT_RESULT_VALUE','REPORT_RESULT_UNIT'],inplace=True)
    df = df[df['REPORT_RESULT_UNIT'].isin(units_to_convert)]

    def unit_conversion(row):
        REPORT_RESULT_VALUE, REPORT_RESULT_UNIT = row.REPORT_RESULT_VALUE, row.REPORT_RESULT_UNIT
        conversion = conversion_factor_dict[REPORT_RESULT_UNIT]
    
        if REPORT_RESULT_UNIT == 'UMOLES/G' or REPORT_RESULT_UNIT == 'umol/g':
            return REPORT_RESULT_VALUE**2
        else:
            return REPORT_RESULT_VALUE*conversion

    df['VALUE_MUGRAM_PER_GRAM'] = df.apply(unit_conversion,axis=1)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    
    return df

# Call Dataframe Filtered to List of Contaminants
def call_filtered_df(filepath, chem_filter_list):
    df = chemical_filter(filepath, chem_filter_list)
    # Convert all values to standardized measurements
    df = chemical_to_moles(df)
    df = df.fillna('0')
    # Add sampling year
    df['SAMPLE_YEAR'] = pd.to_datetime(df['SAMPLE_DATE']).dt.year
    # Add sampling year/month
    df['SAMPLE_YEAR_MONTH'] = df['SAMPLE_DATE'].dt.strftime('%Y-%m')
    return df

# Create 8 COC Dataframe function - returns a dataframe
def call_8coc_df(filepath):
    subset8_df = chemical_filter(filepath, contaminant_list_8COCs)
    # Convert all values to standardized measurements
    subset8_df = chemical_to_moles(subset8_df)
    subset8_df = subset8_df.fillna('0')
    # Add sampling year
    subset8_df['SAMPLE_YEAR'] = pd.to_datetime(subset8_df['SAMPLE_DATE']).dt.year
    subset8_df['SAMPLE_YEAR_MONTH'] = pd.to_datetime(subset8_df['SAMPLE_DATE']).dt.strftime('%Y-%m')
    return subset8_df

# Create 30 COC Dataframe
def call_30_df(filepath):
    subset30_df = chemical_filter(filepath, contaminant_list_30)
    # Convert all values to standardized measurements
    subset30_df = chemical_to_moles(subset30_df)
    subset30_df = subset30_df.fillna('0')
    # Add sampling year
    subset30_df['SAMPLE_YEAR'] = pd.to_datetime(subset30_df['SAMPLE_DATE']).dt.year
    subset30_df['SAMPLE_YEAR_MONTH'] = pd.to_datetime(subset30_df['SAMPLE_DATE']).dt.strftime('%Y-%m')
    return subset30_df

# Call Average Sample Value at Location Individual Dataframe for each of 8 COCs
def call_coc_density_df(subset8_df, coc):
    coc_df = subset8_df[subset8_df['CHEMICAL_NAME'] == eight_coc_dict[coc]]
    coc_df = coc_df.groupby(["LATITUDE", "LONGITUDE"]).mean()
    coc_df['CHEMICAL_NAME'] = eight_coc_dict[coc]
    coc_df['SAMPLE_YEAR'] = coc_df['SAMPLE_YEAR'].astype('int')
    coc_df.reset_index(inplace=True)
    return coc_df


# FUNCTIONS FOR VISUALS

# Create Line Plot of 8 COCs
def lineplot_8cocs(subset8_df):
    subset8_grouped = subset8_df.groupby(['SAMPLE_YEAR_MONTH','CHEMICAL_NAME']).mean()
    subset8_grouped.fillna('0')
    eight_coc_lineplot = subset8_grouped['REPORT_RESULT_VALUE'].hvplot.line(
        x='SAMPLE_YEAR_MONTH',
        groupby='CHEMICAL_NAME',
        title='Volatile Chemical Measurements in the Passaic River Basin',
        xlabel='sample year and month',
        ylabel='average concentration (ug/g)',
        rot=90)
    return eight_coc_lineplot

# Industry Dataframe
industry_filepath = '../notebooks/libs/clean_industry_coordinates.csv'
industry_df = pd.read_csv(industry_filepath, parse_dates=True, infer_datetime_format=True)

load_dotenv()
map_box_api = os.getenv("mapbox")
px.set_mapbox_access_token(map_box_api)

# All Industry Figure
def call_industry_figure(industry_df):
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df,
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])
    
    industry_fig.update_mapboxes(
        bearing=0,
        accesstoken=map_box_api,
        center=dict(
            lat=40.757,
            lon=-74.146
        ),
        pitch=0,
        zoom=12)

    return industry_fig

# Filtered Industry Figure
def filter_industry_figure(industry):
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == industry],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        title=f'Industry Sites - {industry}',
        hover_data=['Description_of_Operations', 'Site_Operator'])
    return industry_fig

# Density Map Plots
def coc_density_plot(coc_density_df, radius):
    px.set_mapbox_access_token(map_box_api)
    coc_fig = px.density_mapbox(
    coc_density_df[['VALUE_MUMOL_PER_GRAM', 'LATITUDE', 'LONGITUDE', 'CHEMICAL_NAME', 'SAMPLE_YEAR']],
    lat='LATITUDE',
    lon='LONGITUDE',
    zoom=12,
    height=1000,
    width=1200,
    z="VALUE_MUMOL_PER_GRAM",
    radius=radius,
    hover_data=['CHEMICAL_NAME', 'VALUE_MUMOL_PER_GRAM']
    )
    return coc_fig

# Special Industry Plot with Markers Written On
def label_industry_fig():
    lats = industry_df['Latitude']
    lons = industry_df['Longitude']
    text = industry_df['Site_Operator']

    fig = go.Figure(go.Scattermapbox(lat=lats,
                                       lon=lons,
                                       mode='text+markers',
                                       text=text,
                                       textposition='top center',
                                       marker_size=12, marker_color='red'))
    fig.update_layout(title_text ='Historic Industry and Operations', 
                          title_x =0.5, 
                          width=1000, 
                          height=1200,
                          mapbox = dict(center= dict(lat=40.757, lon=-74.146),
                                        accesstoken=map_box_api,
                                        zoom=12,
                                        style="light"))
    return(fig)

# Overlay Figures
def overlay_coc_industry_figure(industry_fig, coc_fig):
    px.set_mapbox_access_token(map_box_api)
    industry_coc_fig = industry_fig.add_trace(coc_fig.data[0])
    return industry_coc_fig

# Line Plot for 30 COCs

def avg_30_df(filepath):
    subset30_df = call_30_df(filepath)
    more_filtered_columns = subset30_df[["SAMPLE_YEAR","CHEMICAL_NAME", "VALUE_MUMOL_PER_GRAM"]]
    mean_concentrations_set30 = more_filtered_columns.groupby(["SAMPLE_YEAR","CHEMICAL_NAME"]).mean()
    return mean_concentrations_set30

def average_concentration_bar():
    concentration_bar_plot = mean_concentrations_set30["VALUE_MUMOL_PER_GRAM"].hvplot.bar(
        x='SAMPLE_YEAR', 
        y='VALUE_MUMOL_PER_GRAM', 
        xlabel='Year', 
        ylabel='Average Concentration (umol/g)', 
        title= 'Average Concentration By Year', 
        groupby='CHEMICAL_NAME')
    return concentration_bar_plot

def average_concentration_line():
    concentration_line_plot = mean_concentrations_set30["VALUE_MUMOL_PER_GRAM"].hvplot.line(
        x='SAMPLE_YEAR', 
        y='VALUE_MUMOL_PER_GRAM', 
        xlabel='Year', 
        ylabel='Average Concentration (umol/g)', 
        title= 'Average Concentration By Year', 
        groupby='CHEMICAL_NAME')
    return concentration_line_plot



# STOCK VARIABLES
filepath = '../data/cleandata'

# Line Plots
mean_concentrations_set30 = avg_30_df(filepath)
subset30_bar = average_concentration_bar()
subset30_line = average_concentration_line()

# 8 COC full dataframe and individual dataframes
subset8_df = call_8coc_df(filepath)
copper_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Copper"]
lead_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Lead"]
mercury_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Mercury"]
dioxin_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "2,3,7,8-Tetrachlorodibenzo-p-dioxin"]
dieldrin_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Dieldrin"]
DDT_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "p,p'-DDT"]
pah_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Benzo(a)pyrene"]
pcb_df = subset8_df[subset8_df['CHEMICAL_NAME'] == "Pentachlorobiphenyl; 3,3',4,4',5- (PCB 126)"]

# Average Sample Values at Location Dataframes for Density Plot
copper_density_df = call_coc_density_df(subset8_df, "copper")
lead_density_df = call_coc_density_df(subset8_df, "lead")
mercury_density_df = call_coc_density_df(subset8_df, "mercury")
dioxin_density_df = call_coc_density_df(subset8_df, "dioxin")
dieldrin_density_df = call_coc_density_df(subset8_df, "dieldrin")
DDT_density_df = call_coc_density_df(subset8_df, "DDT")
pah_density_df = call_coc_density_df(subset8_df, "pah")
pcb_density_df = call_coc_density_df(subset8_df, "pcb")

# Line Plot
eight_coc_lineplot = lineplot_8cocs(subset8_df)

# Labeled Industry Figure
industry_label_fig = label_industry_fig()
coc_scatter_fig = px.scatter_mapbox(
    subset8_df,
    lat="LATITUDE",
    lon="LONGITUDE",
    size="VALUE_MUMOL_PER_GRAM",
    size_max=50, 
    zoom=12,
    height=1000,
    width=1200,
    title='Eight Contaminants of Concern',
    color="CHEMICAL_NAME",
    hover_data=["SAMPLE_DATE"],
)
industry_all_coc_fig = overlay_coc_industry_figure(coc_scatter_fig, industry_label_fig)

# Industry Figure
industry_fig = call_industry_figure(industry_df)

# Filtered Industry Figures
copper_industry_fig = filter_industry_figure('copper')
lead_industry_fig = filter_industry_figure('lead')
mercury_industry_fig = filter_industry_figure('mercury')
dioxin_industry_fig = filter_industry_figure('dioxins')
dieldrin_industry_fig = filter_industry_figure('dieldrin')
DDT_industry_fig = filter_industry_figure('DDT')
pah_industry_fig = filter_industry_figure('PAHs')
pcb_industry_fig = filter_industry_figure('PCBs')

# Density Figures
copper_density_fig = coc_density_plot(copper_density_df, 10)
lead_density_fig = coc_density_plot(lead_density_df, 10)
mercury_density_fig = coc_density_plot(mercury_density_df, 10)
dioxin_density_fig = coc_density_plot(dioxin_density_df, 10)
dieldrin_density_fig = coc_density_plot(dieldrin_density_df, 10)
DDT_density_fig = coc_density_plot(DDT_density_df, 10)
pah_density_fig = coc_density_plot(pah_density_df, 10)
pcb_density_fig = coc_density_plot(pcb_density_df, 10)

# Density Overlay Industry Figures
copper_overlay_fig = overlay_coc_industry_figure(copper_industry_fig, copper_density_fig)
lead_overlay_fig = overlay_coc_industry_figure(lead_industry_fig, lead_density_fig)
mercury_overlay_fig = overlay_coc_industry_figure(mercury_industry_fig, mercury_density_fig)
dioxin_overlay_fig = overlay_coc_industry_figure(dioxin_industry_fig, dioxin_density_fig)
dieldrin_overlay_fig = overlay_coc_industry_figure(dieldrin_industry_fig, dieldrin_density_fig)
DDT_overlay_fig = overlay_coc_industry_figure(DDT_industry_fig, DDT_density_fig)
pah_overlay_fig = overlay_coc_industry_figure(pah_industry_fig, pah_density_fig)
pcb_overlay_fig = overlay_coc_industry_figure(pcb_industry_fig, pcb_density_fig)
