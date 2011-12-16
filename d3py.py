import pandas
import json
import os
import webbrowser

class Figure(object):
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.js = """
function(data){

vis = d3.select('#chart')
    .append('svg:g');
        """
        self.css = ""
        fh = open('d3py_template.html')
        self.html = fh.read()
        fh.close()
    
    def add_geom(self, geom):
        self.js += geom.js
        self.css += geom.css
    
    def __add__(self, geom):
        self.add_geom(geom)
    
    def data_to_json(self):
        d = [ 
            dict([
                (colname, row[i]) 
                for i,colname in enumerate(self.data.columns)
            ])
            for row in self.data.values
        ]
        return json.dumps(d)
    
    def show():
        # close javascript callback
        self.js += "}"
        # make directory
        os.mkdir("%s"%name)
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
        # start server
        pass
        # fire up a browser 
        webbrowser.open_new_tab("d3py.html?show=%s"%name)

class Geom(object):
    def __init__(self):
        self.js = ""
        self.css = ""
    
    def build_js(self):
        raise NotImplementedError
    
    def build_css(self):
        raise NotImplementedError
    

class Line(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self)
        self.x = x
        self.y = y
        self.styles = kwargs
        self.build_js()
        self.build_css()
        
    def build_js(self):
        
        # add the line (actually there's a shit ton todo before this)
        self.js += """
var line = d3.svg.line()
    .x(function(d,i) { return d.%s; })
    .y(function(d) {return d.%s; })
        """%(self.x, self.y)
        
        # append the line to the g element
        self.js += """
g.append('svg:path')
    .attr('d', line(data))
        """
        
    def build_css(self):
        self.css = "line {\n"
        for key in self.styles:
            self.css += "%s: %s\n"%(key, kwargs[key])
        self.css += "}"
        
if __name__ == "__main__":
    import numpy as np
    
    df = pandas.DataFrame({
        "time" : [1,2,3,4,5],
        "temp" : np.random.rand(5)
    })
    
    fig = Figure(df, name="random_temp") # instantiates the figure object
    fig += Line(x="time", y="temp") # adds a line
    fig.show() # writes 3 files, then draws some beautiful thing in Chrome