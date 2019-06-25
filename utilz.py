from datetime import datetime as dt
from math import sqrt

# t2 = datetime.datetime.now()
# d = t2 - t1
# d.total_seconds()


def timer(t,label):
    duration = dt.now() - t
    duration = duration.total_seconds()
    print ("{} took {}".format(label, duration))

# def getDistance(movements):
#     totalDistance = 0
#     distance = 0
#     for i in movements:
#         distance = sqrt(((i[1][0] - i[0][0]) ** 2) + ((i[1][1] - i[0][1]) ** 2))
#         totalDistance += distance
#     return totalDistance

def calc_distance(x1,y1,x2,y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def guess_seek_threshold(positions):

    minZ = 0
    maxZ = 0
    for i in positions:
        if "Z" in i.keys():
            #print(i["Z"])
            minZ = min(minZ, i["Z"])
            maxZ = max(maxZ, i["Z"])
    return (minZ+maxZ)/2


def getMaxXY(positions):
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    for i in positions:

        if "X" in i.keys():
            #print(i["Z"])
            minX = min(minX, i["X"])
            maxX = max(maxX, i["X"])
        if "Y" in i.keys():
            #print(i["Z"])
            minY = min(minY, i["Y"])
            maxY = max(maxY, i["Y"])
    return((maxX, maxY))


def open_file(gcode_path, file_name):
    with open("{}{}".format(gcode_path, file_name)) as file:
        opened = file.read()

    return opened


def pprint(iterable_input):
    for i in iterable_input:
        print(i)