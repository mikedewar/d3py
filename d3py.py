import pandas
import json
import os
import webbrowser
import SimpleHTTPServer
import SocketServer
import subproceses

def serve(self):
    """
    start up a server to serve the files for this vis. 
        
    TODO NOTE THAT THIS SHOULD BE A SEPARATE PROCESS OH MY GOD!!! PLEASE SOMEONE FIX THIS IF POSS
    """
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "you can find your chart at http://localhost:%s/%s/%s.html"%(PORT,self.name,self.name)
    httpd.serve_forever()
    "python -m SimpleHTTPServer 8000"




class D3object(object):
    def add_js(self,s):
        """
        adds a line of javascript to the js object. Tries to do
        some nice formatting
        """
        if not (s.startswith("function") or s.startswith("}")):
            self.js += "\t"
        if s.startswith('.'):
            self.js += "\t"
        self.js += s
        self.js += "\n"
        if s.endswith(";"):
            self.js += "\n"
    
    def add_css(self,s):
        if not (("{" in s) or ("}" in s)):
            self.css += "\t"
        self.css += s
        self.css += "\n"
    

class Figure(D3object):
    def __init__(self, data, name, width=400, height=100, margin=10, port=8000):
        """
        data : dataFrame
            data used for the plot. This dataFrame is column centric
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
        """
        # store data
        self.data = data
        self.name = name
        # port
        self.port = port
        # initialise strings
        self.js = ""
        self.css = ""
        # 
        self.add_js("function draw(data){")
        self.add_js("g = d3.select('#chart')")
        self.add_js(".append('svg:svg')")
        self.add_js(".append('svg:g');")
        # we start the html using a template - it's pretty simple
        fh = open('static/d3py_template.html')
        self.html = fh.read()
        fh.close()
        self.html = self.html.replace("{{ port }}", str(port))
        self.html = self.html.replace("{{ name }}", name)
        # build up the basic css
        self.add_css("#chart {width: %spx; height: %spx;}"%(width, height))
        # we make some structures that all the geoms can use
        # we build the ranges up so that each column can be used as an x or y axis
        # this is a bit hacky, but should suffice for now
        self.add_js("var scales = {")
        for colname in data.columns:
            self.add_js("\t%s_y: d3.scale.linear()"%colname)
            self.add_js(".domain([%s, %s])"%(max(data[colname]), min(data[colname])))
            self.add_js(".range([%s, %s]),"%(margin, height-margin))
            self.add_js("\t%s_x: d3.scale.linear()"%colname)
            self.add_js(".domain([%s, %s])"%(min(data[colname]), max(data[colname])))
            self.add_js(".range([%s, %s]),"%(margin, width-margin))
        self.add_js("};")
        
    
    def add_geom(self, geom):
        errmsg = "the %s geom requests %s which is not in our dataFrame!"
        for p in geom.params:
            if p:
                assert p in self.data, errmsg%(geom.name, p)
        self.js += geom.js
        self.css += geom.css
    
    def __add__(self, geom):
        self.add_geom(geom)
    
    def __iadd__(self, geom):
        self.add_geom(geom)
        return self
    
    def data_to_json(self):
        d = [ 
            dict([
                (colname, row[i]) 
                for i,colname in enumerate(self.data.columns)
            ])
            for row in self.data.values
        ]
        return json.dumps(d)
    
    def _close_js(self):
        """
        closes the javascript. Used in show, but you might also want this
        if you want to play with the callback
        """
        self.add_js("}")
    
    def show(self):
        # close javascript callback
        self._close_js()
        # make directory
        try:
            os.mkdir("%s"%self.name)
        except OSError:
            pass
        # write data
        fh = open("%s/%s.json"%(self.name, self.name), 'w')
        fh.write(self.data_to_json())
        fh.close()
        # write css
        fh = open("%s/%s.css"%(self.name, self.name), 'w')
        fh.write(self.css)
        fh.close()
        # write javascript
        fh = open("%s/%s.js"%(self.name, self.name), 'w')
        fh.write(self.js)
        fh.close()
        # write html
        fh = open("%s/%s.html"%(self.name,self.name),'w')
        fh.write(self.html)
        fh.close()
        # start server
        self.serve()
        # fire up a browser 
        webbrowser.open_new_tab("d3py.html?show=%s"%name)

if __name__ == "__main__":
    import numpy as np
    from geoms import *
    
    # some test data
    T = 10
    df = pandas.DataFrame({
        "time" : range(T),
        "pressure": np.random.rand(T),
        "temp" : np.random.rand(T)
    })
    # draw, psuedo ggplot style
    fig = Figure(df, name="random_temp", width=300, height=300) # instantiates the figure object
    #fig += Line(x="time", y="temp", stroke="red") # adds a red line
    fig += Point(x="pressure", y="temp", fill="red") # adds red points

    fig1 = Figure(df, name="random_temp") # instantiates the figure object
    fig1 += Bar(x="time", y="temp")
    fig1.show() # writes 3 files, then draws some beautiful thing in Chrome
