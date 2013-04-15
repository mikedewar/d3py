import d3py
import pandas as pd
import random

x = range(0, 21, 1)
y = [random.randint(25, 100) for num in range(0, 21, 1)]

df = pd.DataFrame({'x': x, 'y': y})

#Create Pandas figure
fig = d3py.PandasFigure(df, 'd3py_area', port=8080, columns=['x', 'y'])

#Add Vega Area plot
fig += d3py.vega.Area()

#Add interpolation to figure data
fig.vega + ({'value': 'basis'}, 'marks', 0, 'properties', 'enter', 
            'interpolate')
fig.show()