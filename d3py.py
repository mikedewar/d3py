import os
import webbrowser
import json
import numpy as np

path_to_this_file = os.path.abspath( __file__ )
temp_json = os.path.join(os.path.dirname(path_to_this_file), "static/temp.json")

def line(x, y, xlabel="x", ylabel="y", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(x, y)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    fh = open(temp_json,'w')
    json.dump(data,fh)
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/line",new=True)
    elif refresh == "manual":
        pass
    

def histogram(x, xlabel="x", ylabel="p(x)", refresh="new", **kwargs):
    
    values, edges = np.histogram(x, **kwargs)
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(edges, values)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    
    fh = open(temp_json,'w')
    json.dump(data,fh)
    fh.close()
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/histogram",new=True)
    elif refresh == "manual":
        pass


def scatter(x, y, c, xlabel="x", ylabel="y", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi, "c":ci} for (xi, yi, ci) in zip(x,y,c)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    
    fh = open(temp_json,'w')
    json.dump(data,fh)
    fh.close()
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/scatter",new=True)
    elif refresh == "manual":
        pass


if __name__ == "__main__":

    import d3py
    
    if False:
        # line plot example
        T = 5*np.pi
        x = np.linspace(-T,T,100)
        a = 0.05
        y = np.exp(-a*x) * np.sin(x)
        d3py.line(x, y, xlabel="time", ylabel="value")
    
    if False:
        # histogram example
        d3py.histogram(np.random.standard_normal(1000), density=True)
    
    if True:
        # scatter example
        n = 400
        d1 = np.random.multivariate_normal([1,1], 0.5*np.eye(2), size=n)
        d2 = list(np.random.multivariate_normal([-1,-1], 2*np.eye(2), size=n))
        
        x = [d[0] for d in d1] + [d[0] for d in d2]
        y = [d[1] for d in d1] + [d[1] for d in d2]
        c = ["crimson" for i in range(n)] + ["green" for i in range(n)]
        d3py.scatter(x, y, c, xlabel="pigs", ylabel="cows")
        
        
        
    
