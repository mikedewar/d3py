import webbrowser
import json


def plot(x, y, xlabel="x", ylabel="y", refresh="new"):
    
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
    
    T = 10*np.pi
    x = np.linspace(0,T,100)
    a = 0.05
    y = np.exp(-a*x) * np.sin(x)
    plot(x, y, xlabel="time", ylabel="value", refresh="manual")
    