import pandas
import json
import os
import webbrowser
import SimpleHTTPServer
import SocketServer

import lib

class Figure(object):
    def __init__(self, data, name, port=8000):
        """
        data : dataFrame
            data used for the plot. This dataFrame is column centric
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
        """
        self.add_js = lib.add_js
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
        self.add_js(".append('svg:g');")
        # we start the html using a template - it's pretty simple
        fh = open('static/d3py_template.html')
        self.html = fh.read()
        fh.close()
        self.html = self.html.replace("{{ port }}", str(port))
        self.html = self.html.replace("{{ name }}", name)
    
    def add_geom(self, geom):
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
    
    def show(self):
        # close javascript callback
        self._close_js()
        print self.js
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
    
    # some test data
    T = 100
    df = pandas.DataFrame({
        "time" : range(T),
        "temp" : np.random.rand(T)
    })
    # draw, psuedo ggplot style
    fig = Figure(df, name="random_temp") # instantiates the figure object
    fig += Line(x="time", y="temp", color="red") # adds a red line
    fig.show() # writes 3 files, then draws some beautiful thing in Chrome