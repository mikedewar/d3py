import d3py
import pandas as pd
import random

x = ['apples', 'oranges', 'grapes', 'bananas', 'plums', 'blackberries']
y = [10, 17, 43, 23, 31, 18]

df = pd.DataFrame({'x': x, 'y': y})

#Create Pandas figure
fig = d3py.PandasFigure(df, 'd3py_area', port=8000, columns=['x', 'y'])

#Add Vega Area plot
fig += d3py.vega.Bar()

#Show figure
fig.show()