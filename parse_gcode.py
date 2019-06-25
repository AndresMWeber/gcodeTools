import pygcode
from pygcode import Line, Machine, GCodeRapidMove, GCodeLinearMove, GCodeDwell
from utilz import *

def get_positions(data):
    t1 = dt.now()
    machine = Machine()
    positions = []
    last = []
    for i in data.split('\n'):
        line = Line(i)
        block = line.block.gcodes
        for g in block:
            machine.process_gcodes(g)
            keys = []
            for key in machine.pos.values.keys():

                keys.append(machine.pos.values[key])
            #positions.append(keys)
            position = machine.pos.values
            if position != last:
                positions.append(position)
            last = position
    timer(t1, "processing gcode")


    return positions


def get_movements(positions):
    movements = []  # arrange data as movements from one point to another

    lastPos = [0, 0, 0]

    for p in positions:
        newPos = [p['X'], p['Y'], p['Z']]
        movements.append([lastPos, newPos])
        lastPos = newPos

    return movements

def get_strokes(positions, seek_threshold):
    strokes = []
    for m in get_movements(positions):

        # if m[0][2] > threshold:
        #     seeks.append(    [(m[0][0], m[0][1]), (m[1][0], m[1][1])]   )

        if m[0][2] <= seek_threshold:
            strokes.append([(m[0][0], m[0][1]), (m[1][0], m[1][1])])

    return strokes


# group connected strokes into cities
def get_cities(positions, seek_threshold):
    start_position = positions[0]
    seeks = []
    cities = []
    current_pos = [positions[0]]
    city = []

    for x, position in enumerate(positions):
        # print("| x", i['X'],"| y", i['Y'],"| z", i['Z'])
        if x == 0:
            current_pos = [positions[0]]
            if current_pos[0]['Z'] <= seek_threshold:
                city.append(position)

        else:

            if position['Z'] <= seek_threshold:

                city.append(position)


            else:
                if city:
                    cities.append(city)
                    city = []
    return cities