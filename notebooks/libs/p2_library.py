# Define function to create the rest of the density plots
def coc_plot(coc_df):
        coc_fig = px.density_mapbox(
        coc_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        zoom=12,
        height=1000,
        width=1000,
        animation_frame="CHEMICAL_NAME",
        radius=15,
        hover_data=['CHEMICAL_NAME']
        )
        return coc_fig

# Create all COC density plots using coc_plot function
copper_fig = coc_plot(copper_df)
lead_fig = coc_plot(lead_df)
mercury_fig = coc_plot(mercury_df)
dioxin_fig = coc_plot(dioxin_df)
dieldrin_fig = coc_plot(dieldrin_df)
DDT_fig = coc_plot(DDT_df)
pah_fig = coc_plot(pah_df)
pcb_fig = coc_plot(pcb_df)

#Each individual plot
def copper_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'copper'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(copper_fig.data[0])
    return industry_fig

def lead_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'lead'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(lead_fig.data[0])
    return industry_fig

def mercury_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'mercury'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(mercury_fig.data[0])
    return industry_fig

def dioxin_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'dioxins'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(dioxin_fig.data[0])
    return industry_fig

def dieldrin_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'dieldrin'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(dieldrin_fig.data[0])
    return industry_fig

def ddt_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'DDT'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(DDT_fig.data[0])
    return industry_fig

def pah_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'PAHs'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(pah_fig.data[0])
    return industry_fig

def pcb_industry_figure():
    px.set_mapbox_access_token(map_box_api)
    industry_fig = px.scatter_mapbox(
        industry_df.loc[industry_df['Main_Contaminant _Category'] == 'PCBs'],
        lat="Latitude",
        lon="Longitude",
        zoom=12,
        height=1000,
        width=1200,
        color='Main_Contaminant _Category',
        hover_data=['Description_of_Operations', 'Site_Operator'])

    industry_fig.add_trace(pcb_fig.data[0])
    return industry_fig