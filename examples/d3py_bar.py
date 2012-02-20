import numpy as np
import pandas
import d3py

df = pandas.DataFrame({
    "count" : [1,4,7,3,2,9],
    "apple_type" : ["a", "b", "c", "d", "e", "f"]
})

with d3py.Figure(df) as p:
    p += d3py.Bar(x = "apple_type", y = "count", fill = "MediumAquamarine")
    p += d3py.xAxis(x = "apple_type")
    p.show()
