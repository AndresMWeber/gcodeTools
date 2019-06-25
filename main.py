
import numpy as np
import random
from datetime import datetime as dt
from math import sqrt
from timeit import timeit
# import matplotlib.pyplot as plt
import pygcode
import test_data
# from matplotlib.collections import LineCollection
from parse_gcode import *
from pygcode import Line, Machine, GCodeRapidMove, GCodeLinearMove, GCodeDwell
from utilz import *



from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import MultiLine
from bokeh.io import curdoc, show




data = test_data.inkscape_long
#data = test_data.inkscape_short
# data = test_data.illustrator_long
#data = test_data.text
#data = test_data.square

gcode_path = '/bish/project/plotter/gcode/'
file_name = 'potato_0002'
# file_name = 'bunny_0005'
# file_name = 'makeblock.cnc.gcode'
#file_name = 'fish.cnc.gcode'

#data = open_file(gcode_path, file_name)


positions = get_positions(data)
seek_threshold = guess_seek_threshold(positions)
movements = get_movements(positions)
strokes = get_strokes(positions, seek_threshold)
maxXY = getMaxXY(positions)



cities = get_cities(positions, seek_threshold)
slim_cities = [[i[0]['X'], i[0]['Y'], i[-1]['X'], i[-1]['Y']] for i in cities]  # start x, start y, end x, end y
distance = 0

original_path = [x for x in range(len(slim_cities))]  # sequence in which the original gcode visits the cities

  # randomisation of the sequence

#path = random_path
path = original_path


start_position = positions[0]

def get_random_path(original_path):
    return random.sample(original_path, len(original_path))


def get_distance(path):
    distance = 0
    tour = []
    for loopIndex, city in enumerate(path):
        if loopIndex == 0:
            startIndex = path[0]
            x1 = start_position['X']
            y1 = start_position['Y']
            x2 = slim_cities[startIndex][0]
            y2 = slim_cities[startIndex][1]
            tour.append([(x1, y1), (x2, y2)])
            distance += calc_distance(x1, y1, x2, y2)

        else:
            index = path[loopIndex]
            lastIndex = path[loopIndex - 1]
            x1 = slim_cities[lastIndex][2]
            y1 = slim_cities[lastIndex][3]
            x2 = slim_cities[index][0]
            y2 = slim_cities[index][1]
            tour.append([(x1, y1), (x2, y2)])
            distance += calc_distance(x1, y1, x2, y2)

        return distance

def get_line_collection(path):
    tour = []

    for loopIndex, city in enumerate(path):
        if loopIndex == 0:
            startIndex = path[0]
            x1 = start_position['X']
            y1 = start_position['Y']
            x2 = slim_cities[startIndex][0]
            y2 = slim_cities[startIndex][1]
            tour.append([(x1, y1), (x2, y2)])
            # distance += get_distance(x1, y1, x2, y2)

        else:
            index = path[loopIndex]
            lastIndex = path[loopIndex - 1]
            x1 = slim_cities[lastIndex][2]
            y1 = slim_cities[lastIndex][3]
            x2 = slim_cities[index][0]
            y2 = slim_cities[index][1]
            tour.append([(x1, y1), (x2, y2)])
            # distance += get_distance(x1, y1, x2, y2)

    return tour


def get_bokeh_source(path):

    xs = []
    ys = []
    for loopIndex, city in enumerate(path):
        if loopIndex == 0:
            startIndex = path[0]
            x1 = start_position['X']
            y1 = start_position['Y']
            x2 = slim_cities[startIndex][0]
            y2 = slim_cities[startIndex][1]
            xs.append([x1, x2])
            ys.append([y1,y2])

        else:
            pathIndex = path[loopIndex]
            lastIndex = path[loopIndex -1]
            x1 = slim_cities[lastIndex][2]
            y1 = slim_cities[lastIndex][3]
            x2 = slim_cities[pathIndex][0]
            y2 = slim_cities[pathIndex][1]
            xs.append([x1, x2])
            ys.append([y1,y2])
    return dict(
            xs = xs,
            ys = ys
    )



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

# print(np.random.rand(10,2)*100)

def update():
    bokeh_source = get_bokeh_source(get_random_path(original_path))
    #source.stream(bokeh_source, rollover=50)
    #source.stream(bokeh_source, rollover = None)


random_path = get_random_path(original_path)




path = original_path
source = ColumnDataSource(get_bokeh_source(get_random_path(original_path)))

init_plot()
curdoc().add_periodic_callback(update, 100)