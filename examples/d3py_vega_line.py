import d3py
import pandas as pd
import random

x = range(0, 101, 1)
y = [random.randint(10, 100) for num in range(0, 101, 1)]

df = pd.DataFrame({'x': x, 'y': y})

#Create Pandas figure
fig = d3py.PandasFigure(df, 'd3py_area', port=8000, columns=['x', 'y'])

#Add Vega Area plot
fig += d3py.vega.Line()

#Show figure
fig.show()

