import numpy as np
import d3py
n = 400
d1 = np.random.multivariate_normal([1,1], 0.5*np.eye(2), size=n)
d2 = np.random.multivariate_normal([-1,-1], 2*np.eye(2), size=n)
x = [d[0] for d in d1] + [d[0] for d in d2]
y = [d[1] for d in d1] + [d[1] for d in d2]
c = ["crimson" for i in range(n)] + ["green" for i in range(n)]
d3py.scatter(x, y, c, xlabel="pigs", ylabel="cows")
