import numpy as np
import d3py
import pandas

T = 5*np.pi
x = np.linspace(-T,T,100)
a = 0.05
y = np.exp(-a*x) * np.sin(x)

df = pandas.DataFrame({
    'x' : x,
    'y' : y
})

with d3py.PandasFigure(df, 'd3py_line', width=600, height=200) as fig:
    fig += d3py.geoms.Line('x', 'y', stroke='BlueViolet')
    fig += d3py.xAxis('x')
    fig += d3py.yAxis('y')
    fig.show()
