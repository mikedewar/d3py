from d3py import D3object

class Geom(D3object):
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = ""
        self.css = ""
    
    def build_js(self):
        raise NotImplementedError
    
    def build_css(self):
        raise NotImplementedError
    

class Line(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.debug = True
        self.build_js()
        self.build_css()
        
    def build_js(self):
        # add the line
        self.add_js("var line = d3.svg.line()")
        self.add_js(".x(function(d) { ")
        self.add_js("\t\t\treturn scales.%s_x(d.%s)"%(self.x,self.x))
        self.add_js("\t\t})")
        self.add_js(".y(function(d) { ")
        self.add_js("\t\t\treturn scales.%s_y(d.%s)"%(self.y, self.y))
        self.add_js("\t\t});")
        # append the line to the g element
        self.add_js("g.append('svg:path')")
        self.add_js(".attr('d', line(data))")
        self.add_js(".attr('class', 'geom_line')")
        self.add_js(".attr('id', 'line_%s_%s');"%(self.x,self.y))
        
    def build_css(self):
        # default css
        self.add_css(".geom_line {")
        self.add_css("stroke-width: 1px;")
        self.add_css("stroke: black;")
        self.add_css("fill: none;")
        self.add_css("}")
        
        self.add_css("#line_%s_%s {\n"%(self.x,self.y))
        for key in self.styles:
            self.add_css ("%s: %s\n"%(key, self.styles[key]))
        self.add_css("}")

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self, kwargs)
        raise NotImplementedError

class Point(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self, kwargs)
        raise NotImplementedError
