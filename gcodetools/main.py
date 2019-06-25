import random
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import MultiLine
from bokeh.io import curdoc

from parse_gcode import (guess_seek_threshold,
                         get_positions,
                         get_cities,
                         get_movements,
                         get_strokes,
                         calc_distance)
from utilz import open_file, getMaxXY


x = 'X'
y = 'Y'
gcode_path = './gcode_data/'
file_name = 'inkscape_short.gcode'


class GeneticLoop(object):
    def __init__(self, data):
        self.source = ColumnDataSource(
            self.get_bokeh_source(self.get_random_path(self.original_path)))

        positions = get_positions(data)
        seek_threshold = guess_seek_threshold(positions)
        self.movements = get_movements(positions)
        self.strokes = get_strokes(positions, seek_threshold)
        self.maxXY = getMaxXY(positions)
        self.cities = get_cities(positions, seek_threshold)

        # start x, start y, end x, end y
        self.slim_cities = [[city[0][x], city[0][y], city[-1][y], city[-1][y]]
                            for city in self.cities]
        self.distance = 0

        # sequence in which the original gcode visits the cities
        self.original_path = [x for x in range(len(self.slim_cities))]

        # path = random_path
        self.path = self.original_path
        self.start_position = positions[0]

    @staticmethod
    def get_random_path(original_path):
        return random.sample(original_path, len(original_path))

    def get_distance(self, path):
        distance = 0
        tour = []
        for loopIndex, city in enumerate(path):
            if loopIndex == 0:
                startIndex = path[0]
                x1 = self.start_position[x]
                y1 = self.start_position[y]
                x2 = self.slim_cities[startIndex][0]
                y2 = self.slim_cities[startIndex][1]
                tour.append([(x1, y1), (x2, y2)])
                distance += calc_distance(x1, y1, x2, y2)
            else:
                index = path[loopIndex]
                lastIndex = path[loopIndex - 1]
                x1 = self.slim_cities[lastIndex][2]
                y1 = self.slim_cities[lastIndex][3]
                x2 = self.slim_cities[index][0]
                y2 = self.slim_cities[index][1]
                tour.append([(x1, y1), (x2, y2)])
                distance += calc_distance(x1, y1, x2, y2)
            return distance

    def get_line_collection(self, path):
        tour = []

        for loopIndex, city in enumerate(path):
            if loopIndex == 0:
                startIndex = path[0]
                x1 = self.start_position[x]
                y1 = self.start_position[y]
                x2 = self.slim_cities[startIndex][0]
                y2 = self.slim_cities[startIndex][1]
                tour.append([(x1, y1), (x2, y2)])
            else:
                index = path[loopIndex]
                lastIndex = path[loopIndex - 1]
                x1 = self.slim_cities[lastIndex][2]
                y1 = self.slim_cities[lastIndex][3]
                x2 = self.slim_cities[index][0]
                y2 = self.slim_cities[index][1]
                tour.append([(x1, y1), (x2, y2)])
        return tour

    def get_bokeh_source(self, path):
        xs = []
        ys = []
        for loopIndex, city in enumerate(path):
            if loopIndex == 0:
                startIndex = path[0]
                x1 = self.start_position[x]
                y1 = self.start_position[y]
                x2 = self.slim_cities[startIndex][0]
                y2 = self.slim_cities[startIndex][1]
                xs.append([x1, x2])
                ys.append([y1, y2])

            else:
                pathIndex = path[loopIndex]
                lastIndex = path[loopIndex - 1]
                x1 = self.slim_cities[lastIndex][2]
                y1 = self.slim_cities[lastIndex][3]
                x2 = self.slim_cities[pathIndex][0]
                y2 = self.slim_cities[pathIndex][1]
                xs.append([x1, x2])
                ys.append([y1, y2])
        return dict(xs=xs, ys=ys)

    def update(self):
        self.get_bokeh_source(self.get_random_path(self.original_path))
        self.init_plot(self.source)


def init_plot(source):
    plot = Plot(title=None,
                plot_width=600,
                plot_height=600,
                min_border=0,
                toolbar_location=None)

    glyph = MultiLine(xs="xs", ys="ys",
                      line_color="#8073ac", line_width=0.1)
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    curdoc().add_root(plot)


loop = GeneticLoop(open_file(gcode_path, file_name))
curdoc().add_periodic_callback(loop.update, 100)
