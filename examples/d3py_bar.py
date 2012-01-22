import numpy as np
import pandas
import d3py

df = pandas.DataFrame({
    "count" : [1,4,7,3,2,9],
    "apple_type" : ["a", "b", "c", "d", "e", "f"]
})

p = d3py.Figure(df)
p += d3py.Bar(x="count", y="apple_type")
p.show()

