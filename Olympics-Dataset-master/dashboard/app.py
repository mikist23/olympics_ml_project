import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shiny.express import ui, input, render
from shiny import reactive
from pathlib import Path


ui.page_opts(fillable=True)

# get all NOCs
directory = Path(__file__).parent.parent
nocs = pd.read_csv(f'{directory}/clean-data/noc_regions.csv')
    

with ui.layout_sidebar():
    with ui.sidebar(open='open'):
        ui.input_select("country", "Select a country",nocs.NOC.unique().tolist())
        ui.input_checkbox("winter","Include winter games?",True)
        ui.input_checkbox("medalists","Only include medalists?", True)



    with ui.card():
        "Medals"
        # print medals by country
        @render.plot
        def show_medals():
            get_medals()

    with ui.card():
        "Heatmap of athletes"
        # Heatmap


    with ui.card():
        @render.data_frame
        def results():
            return  results_df().head(100)
    


@reactive.calc
def bios_df():
    directory = Path(__file__).parent.parent
    df = pd.read_csv(f'{directory}/clean-data/bios_locs.csv')
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
    print(medals_by_year.reset_index())