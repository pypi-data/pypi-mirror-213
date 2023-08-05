import biocircuits
import numpy as np
import bokeh.io

def dx_dt(x, y):
    return -1 - x**2 + y

def dy_dt(x, y):
    return 1 + x - y**2

x_range = [-0.5, 0.75]
y_range = [0.5, 1.5]

p = biocircuits.phase_portrait(dx_dt, dy_dt, x_range, y_range)

x_theor = np.linspace(-3, 3, 200)
y_theor = np.linspace(-3, 3, 200)
p.line(x_theor, 1 + x_theor**2, line_width=2, line_color='purple')
p.line(y_theor**2 - 1, y_theor, line_width=2, line_color='tomato')

bokeh.io.show(p)
