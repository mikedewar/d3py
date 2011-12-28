class Geom(object):
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = ""
        self.css = ""
        self.add_js = lib.add_js

    
    def build_js(self):
        raise NotImplementedError
    
    def build_css(self):
        raise NotImplementedError
    

class Line(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.build_js()
        self.build_css()
        
    def build_js(self):
        # add the line (actually there's a shit ton todo before this)
        self.add_js("var line = d3.svg.line()")
        self.add_js(".x(function(d,i) { return d.%s; })"%self.x)
        self.add_js(".y(function(d) {return d.%s; })"%self.y)
        # append the line to the g element
        self.add_js("g.append('svg:path')")
        self.add_js(".attr('d', line(data))")
        self.add_js(".attr('class', 'geom_line')")
        
    def build_css(self):
        self.css = "line {\n"
        for key in self.styles:
            self.css += "%s: %s\n"%(key, self.styles[key])
        self.css += "}"

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self, kwargs)
        raise NotImplementedError

class Point(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self, kwargs)
        raise NotImplementedError
