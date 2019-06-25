import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import MultiLine
from time import sleep
from random import randint


def getData():  # simulate data acquisition
    # run slow algorith
    sleep(1) #simulate slowness of algorithm
    return dict(xs=np.random.rand(50, 2).tolist(), ys=np.random.rand(50, 2).tolist())


# init plot
source = ColumnDataSource(data=getData())

def init_plot():
    plot = Plot(
        title=None, plot_width=600, plot_height=600,
        min_border=0, toolbar_location=None)

    glyph = MultiLine(xs="xs", ys="ys", line_color="#8073ac", line_width=0.1)
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    curdoc().add_root(plot)


# update plot
def update():
    bokeh_source = getData()
    source.data=(bokeh_source)


init_plot()

curdoc().add_periodic_callback(update, 100)
