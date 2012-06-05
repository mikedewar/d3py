import numpy as np
import d3py
import pandas

N = 5
T = 5*np.pi
x = np.linspace(-T,T,N)
y = [10 for i in range(N)]
y0 = [20 for i in range(N)] 

df = pandas.DataFrame({
    'x' : x,
    'y' : y,
    'y0' : y0,
})

with d3py.PandasFigure(df, 'd3py_line', width=600, height=200) as fig:
    fig += d3py.geoms.Area('x', 'y', 'y0')
    fig.show()
