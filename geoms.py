from d3py import D3object
from css import CSS

class Geom(D3object):
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = ""
        self.css = CSS()
    
    def build_js(self):
        raise NotImplementedError
    
    def build_css(self):
        raise NotImplementedError
    

class Line(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.params = [x,y]
        self.debug = True
        self.name = "line"
        self.build_js()
        self.build_css()
        
    def build_js(self):
        # add the line
        self.js = ""
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
        geom_line = {"stroke-width": "1px", "stroke": "black", "fill": None}
        self.css[".geom_line"] = geom_line

        self.css["#line_%s_%s"%(self.x,self.y)] = self.styles

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.name = "bar"
        self.build_js()
        self.build_css()
    
    def build_js(self):
        self.js = ""
        self.add_js("g.selectAll('.bars')")
        self.add_js(".data(data)")
        self.add_js(".enter()")
        self.add_js(".append('svg:rect')")
        self.add_js(".attr('x',function(d) {return scales.%s_x(d.%s)} )"%(self.x,self.x))
        self.add_js(".attr('y',function(d) {")
        self.add_js("return d.%s_y > 0 ? scales.%s_y(d.%s) : scales.%s_y(0);"%(self.y, self.y, self.y, self.y))
        self.add_js("})")
        self.add_js(".attr('width', box_width )")
        self.add_js(".attr('height',function(d) {")
        self.add_js("return d.%s > 0 ? scales.%s_y(0) - scales.%s_y(d.%s) : scales.%s_y(d.%s) - scales.%s_y(0);"%(self.y, self.y, self.y, self.y, self.y, self.y, self.y))
        self.add_js("})")

class Point(Geom):
    def __init__(self,x,y,c=None,**kwargs):
        Geom.__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.c = c
        self.params = [x,y,c]
        self.name = "point"
        self.build_css()
        self.build_js()
    
    def build_css(self):
        point = {"stroke-width"  : "1px",
                 "stroke"        : "black",
                 "fill-opacity"  : 0.3,
                 "stroke-opacity": 1,
                 "fill"          : "blue"}
        self.css[".geom_point"] = point
        # arbitrary styles
        self.css["#point_%s_%s_%s"%(self.x,self.y,self.c)] = self.styles
        
    def build_js(self):
        self.js = ""
        self.add_js("g.selectAll('.geom_point')")
        self.add_js(".data(data)")
        self.add_js(".enter()")
        self.add_js(".append('svg:circle')")
        self.add_js(".attr('cx',function(d) {return scales.%s_x(d.%s);})"%(self.x,self.x))
        self.add_js(".attr('cy',function(d) {return scales.%s_y(d.%s);})"%(self.y,self.y))
        self.add_js(".attr('r', 4 )")
        self.add_js(".attr('class','geom_point')")
        self.add_js(".attr('id','point_%s_%s_%s')"%(self.x,self.y,self.c))
        if self.c:
            self.add_css(".style('fill', function(d) {return d.%s;})"%self.c)

    
