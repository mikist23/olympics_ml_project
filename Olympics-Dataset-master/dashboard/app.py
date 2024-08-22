import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render
from shiny import reactive

ui.page_opts(fillable=True)

with ui.layout_sidebar():
    with ui.sidebar(open='open'):
        ui.input_select("Country", "Select a country",['USA',"IND","MEX"])
        ui.input_checkbox("winter","Include winter games?",True)
        ui.input_checkbox("medalists","Only include medalists?", True)


        @render.data_frame
        def histogram():
            np.random.seed(19680801)
            x = 100 + 15 * np.random.randn(437)
            plt.hist(x, input.n(), density=True)