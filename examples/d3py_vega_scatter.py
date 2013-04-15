import d3py
import pandas as pd
import random

n = 400
df = pd.DataFrame({'d1': np.arange(0,n),'d2': np.random.normal(0, 1, n)})

#Create Pandas figure
fig = d3py.PandasFigure(df, 'd3py_area', port=8000, columns=['d1', 'd2'])

#Add Vega Area plot
fig += d3py.vega.Scatter()

#Show figure
fig.show()

