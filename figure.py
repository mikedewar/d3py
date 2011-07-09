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
    
    T = 100
    x = np.arange(T)
    y = np.random.rand(T)
    
    plot(x,y,xlabel="time", ylabel="value",refresh="manual")
    