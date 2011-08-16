import os
import webbrowser
import json
import numpy as np
import time
import urllib
import logging

path_to_this_file = os.path.abspath( __file__ )
this_path = os.path.dirname(path_to_this_file)
temp_json = os.path.join(this_path, "static/temp_%s.json")


def clear():
    urllib.urlopen("http://localhost:7666/clear")

def draw(mode,refresh="new"):
    if refresh == "new":
        webbrowser.open("http://localhost:7666/%s"%mode,new=True)
    elif refresh == "manual":
        pass

def line(x, y, xlabel="x", ylabel="y", color="crimson", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(x, y)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        },
        "color":color
    }
    fname = temp_json%time.time()
    fh = open(fname,'w')
    json.dump(data,fh)
    
    draw("line")

def timeseries(x, y, xlabel="x", ylabel="y", color="crimson", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(x, y)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        },
        "color":color
    }
    fname = temp_json%time.time()
    fh = open(fname,'w')
    json.dump(data,fh)
    
    draw("timeseries")



def histogram(x, xlabel="x", ylabel="p(x)", refresh="new", **kwargs):
    
    values, edges = np.histogram(x, **kwargs)
    
    data = {
        "values":[{"x":xi, "y":yi} for xi, yi in zip(edges, values)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    
    fh = open(temp_json%time.time(),'w')
    json.dump(data,fh)
    fh.close()


def scatter(x, y, c, xlabel="x", ylabel="y", refresh="new"):
    
    data = {
        "values":[{"x":xi, "y":yi, "c":ci} for (xi, yi, ci) in zip(x,y,c)],
        "labels":{
            "x": xlabel,
            "y": ylabel
        }
    }
    
    fh = open(temp_json%time.time(),'w')
    json.dump(data,fh)
    fh.close()
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/scatter",new=True)
    elif refresh == "manual":
        pass


def bar(values, labels, ylabel="count", refresh="new"):

    data = {
        "values":[
            {"x":xi, "y":yi} 
            for xi, yi in zip(labels, values)
        ],
        "labels":{
            "x": None,
            "y": ylabel
        }
    }
    
    fh = open(temp_json%time.time(),'w')
    json.dump(data,fh)
    fh.close()
    
    if refresh == "new":
        webbrowser.open("http://localhost:7666/bar", new=True)
    elif refresh == "manual":
        pass

clear()

if __name__ == "__main__":

    import d3py
    
    if True:
        # line plot example
        T = 5*np.pi
        x = np.linspace(-T,T,100)
        colours = ["red","blue","green"]
        for a,c in zip([0.1, 0.2, 0.3], colours):
            y = np.exp(-a*x) * np.sin(x)
            d3py.line(x, y, xlabel="time", ylabel="value", color=c)
    
    if False:
        # histogram example
        d3py.histogram(np.random.standard_normal(1000), density=True)
    
    if False:
        # scatter example
        n = 400
        d1 = np.random.multivariate_normal([1,1], 0.5*np.eye(2), size=n)
        d2 = list(np.random.multivariate_normal([-1,-1], 2*np.eye(2), size=n))
        
        x = [d[0] for d in d1] + [d[0] for d in d2]
        y = [d[1] for d in d1] + [d[1] for d in d2]
        c = ["crimson" for i in range(n)] + ["green" for i in range(n)]
        d3py.scatter(x, y, c, xlabel="pigs", ylabel="cows")
        
    if False:
        # bar example
        values = [1,4,7,3,2,9]
        labels = ["a", "b", "c", "d", "e", "f"]
        d3py.bar(values, labels)
    