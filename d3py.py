import webbrowser
import json
import numpy as np

def line(x, y, xlabel="x", ylabel="y", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(x, y)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    
    fh = open("static/temp.json",'w')
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
    
    fh = open("static/temp.json",'w')
    json.dump(data,fh)
    fh.close()
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/histogram",new=True)
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
    
    if True:
        # histogram example
        d3py.histogram(np.random.standard_normal(1000), density=True)
    
    
    