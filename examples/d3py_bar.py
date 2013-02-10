import pandas
import d3py

import logging
logging.basicConfig(level=logging.DEBUG)


df = pandas.DataFrame(
    {
        "count" : [1,4,7,3,2,9],
        "apple_type": ["a", "b", "c", "d", "e", "f"],
    }
)

# use 'with' if you are writing a script and want to serve this up forever
with d3py.PandasFigure(df) as p:
    p += d3py.Bar(x = "apple_type", y = "count", fill = "MediumAquamarine")
    p += d3py.xAxis(x = "apple_type")
    p.show()

# if you are writing in a terminal, use without 'with' to keep everything nice
# and interactive
"""
p = d3py.PandasFigure(df)
p += d3py.Bar(x = "apple_type", y = "count", fill = "MediumAquamarine")
p += d3py.xAxis(x = "apple_type")
p.show()
"""
