import numpy as np
import d3py
import pandas

N = 500
T = 5*np.pi
x = np.linspace(-T,T,N)
y = np.sin(x)
y0 = np.cos(x)

df = pandas.DataFrame({
    'x' : x,
    'y' : y,
    'y0' : y0,
})

with d3py.PandasFigure(df, 'd3py_area', width=500, height=250) as fig:
    fig += d3py.geoms.Area('x', 'y', 'y0')
    fig += d3py.geoms.xAxis('x')
    fig += d3py.geoms.yAxis('y')
    fig.show()
