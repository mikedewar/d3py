import numpy as np
import d3py
data = np.random.standard_normal(1000)
d3py.histogram(data, density=True)
