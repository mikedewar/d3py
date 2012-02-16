import numpy as np
import pandas
from d3py import d3py, geoms
n = 400

df = pandas.DataFrame({
    'd1': np.arange(0,n),
    'd2': np.random.normal(0, 1, n)
})


fig = d3py.Figure(df, "my_figure")
fig += geoms.Point("d1", "d2", fill="red")
fig.show()
