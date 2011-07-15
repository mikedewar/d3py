import webbrowser
import json


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
        webbrowser.open("http://localhost:7666/base",new=True)
    elif refresh == "manual":
        pass
    


if __name__ == "__main__":
    import numpy as np
    import d3py
    
    T = 5*np.pi
    x = np.linspace(-T,T,100)
    a = 0.05
    y = np.exp(-a*x) * np.sin(x)
    d3py.line(x, y, xlabel="time", ylabel="value")
    