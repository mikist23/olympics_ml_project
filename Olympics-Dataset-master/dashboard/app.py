import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shiny.express import ui, input, render
from shiny import reactive
from pathlib import Path


ui.page_opts(fillable=True)


    

with ui.layout_sidebar():
    with ui.sidebar(open='open'):
        ui.input_select("Country", "Select a country",['USA',"IND","MEX"])
        ui.input_checkbox("winter","Include winter games?",True)
        ui.input_checkbox("medalists","Only include medalists?", True)


    @render.data_frame
    def results():
        return  results_df().head(100)
    

@reactive.calc
def results_df():
    directory = Path(__file__).parent.parent
    df = pd.read_csv(f'{directory}/clean-data/bios_locs.csv')
    return df