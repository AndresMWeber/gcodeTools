import test_data


data = test_data.inkscape_long
data = test_data.inkscape_short
data = test_data.illustrator_long
data = test_data.text
#data = test_data.square


f = open("square.gcode", "a")
f.write(data)
f.close()


