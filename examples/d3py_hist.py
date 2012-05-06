import pandas
import d3py
import numpy as np

x = np.random.gamma(1, size=100)
count, bins = np.histogram(x)

df = pandas.DataFrame({
    "count" : count,
    "apple_type" : bins[:-1]
})

with d3py.Figure(df) as p:
    p += d3py.Bar(x="apple_type", y = "count", fill = "MediumAquamarine")
    p += d3py.xAxis(x="apple_type", label="Apple Type")
    p += d3py.yAxis(y="count", label="Number")
    p.show()
