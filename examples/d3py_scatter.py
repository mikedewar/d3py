import numpy as np
import pandas
import d3py
n = 400

df = pandas.DataFrame({
    'd1': np.arange(0,n),
    'd2': np.random.normal(0, 1, n)
})

with d3py.Figure(df, "my_figure", width=400, height=400) as fig:
    fig += d3py.Point("d1", "d2", fill="red")
    fig += d3py.xAxis('d1')
    fig.show()
