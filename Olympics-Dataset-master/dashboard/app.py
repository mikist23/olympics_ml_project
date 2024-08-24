import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shiny.express import ui, input, render
from shiny import reactive
from pathlib import Path
import folium
from folium.plugins import HeatMap


ui.page_opts()

# get all NOCs
directory = Path(__file__).parent.parent
nocs = pd.read_csv(f'{directory}/clean-data/noc_regions.csv')
nocs = nocs.sort_values('region', ascending=True)
region_to_noc = dict(zip(nocs['NOC'],nocs['region']))
    

with ui.layout_sidebar():
    with ui.sidebar(open='open'):
        ui.input_select("country", "Select a country",region_to_noc)
        ui.input_checkbox("winter","Include winter games?",True)
        ui.input_checkbox("medalists","Only include medalists?", True)



    with ui.card():
        "Medals"
        # print medals by country
        @render.plot
        def show_medals():
            df = get_medals()
            plt.plot(df['year'], df['medal'])
            plt.xlabel('Year')
            plt.ylabel('Medal Count')
            plt.title("Medals by Year")


    with ui.card():
        "Heatmap of athletes"
        # Heatmap
        @render.ui
        def show_heatmap():
            df = bios_df()
            m = folium.Map(location=[df['lat'].mean(), df['long'].mean()], zoom_start=2)
            heat_data = [[row['lat'], row['long']] for index , row in df.iterrows()]
            HeatMap(heat_data).add_to(m)
            return m



    with ui.card():
        @render.data_frame
        def results():
            return  results_df().head(100)
    


@reactive.calc
def bios_df():
    directory = Path(__file__).parent.parent
    df = pd.read_csv(f'{directory}/clean-data/bios_locs.csv')
    df = df[df['born_country'] == input.country()]
    df = df[df['lat'].notna() & df['long'].notna()]
    return df


@reactive.calc
def results_df():
    directory = Path(__file__).parent.parent
    df = pd.read_csv(f'{directory}/clean-data/results.csv')
    df = df[df['noc'] == input.country()]

    if not input.winter():
        df = df[df['type'] == 'Summer']
    if input.medalists():
        df = df[df['medal'].notna()]

    return df

@reactive.calc
def get_medals():
    results = results_df()
    medals = results[(results['medal'].notna()) & (~results['event'].str.endswith('(YOG)'))]
    medals_filtered = medals.drop_duplicates(['year','type','discipline','noc','event','medal'])
    medals_by_year = medals_filtered.groupby(['noc', 'year'])['medal'].count().loc[input.country()]
    return medals_by_year.reset_index()