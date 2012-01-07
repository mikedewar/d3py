import numpy as np
import d3py
T = 5*np.pi
x = np.linspace(-T,T,100)
a = 0.05
y = np.exp(-a*x) * np.sin(x)
d3py.line(x, y, xlabel="time", ylabel="value")
