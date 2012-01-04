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
        self.params = [x,y]
        self.debug = True
        self.name = "line"
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
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.build_js()
        self.build_css()
    
    def build_js(self):
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
        self.add_css(".geom_point {")
        self.add_css("stroke-width: 1px;")
        self.add_css("stroke: black;")
        self.add_css("fill-opacity: 0.3;")
        self.add_css("stroke-opacity: 1;")
        self.add_css("fill: blue;")
        self.add_css("}")
        # arbitrary styles
        self.add_css("#point_%s_%s_%s {\n"%(self.x,self.y,self.c))
        for key in self.styles:
            self.add_css ("%s: %s\n"%(key, self.styles[key]))
        self.add_css("}")
        
    def build_js(self):
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

    
