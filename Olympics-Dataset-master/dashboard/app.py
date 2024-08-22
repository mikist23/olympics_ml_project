import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render

ui.page_opts(fillable=True)

with ui.layout_sidebar():
    with ui.sidebr():
        ui.input_select("Country", "Select a country")


        @render.plot(aalt="Ahistogram")
        def histogram():
            np.random.seed(19680801)
            x = 100 + 15 * np.randn(437)
            plt.hist(x, input.n(), density=True)