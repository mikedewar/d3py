from d3py import D3object
from css import CSS
import javascript as JS

class Geom(D3object):
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = JS.JavaScript()
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
        x_fxn = JS.Function(None, "d", "return scales.%s_x(d.%s)"%(self.x,self.x))
        y_fxn = JS.Function(None, "d", "return scales.%s_y(d.%s)"%(self.y,self.y))

        self.js = JS.JavaScript()
        self.js += "var line = " + JS.Object("d3.svg").add_attribute("line") \
                                                      .add_attribute("x", x_fxn) \
                                                      .add_attribute("y", y_fxn)

        self.js += JS.Object("g").append("'svg:path'") \
                                 .attr("'d'", "line(data)") \
                                 .attr("'class'", "'geom_line'") \
                                 .attr("'id'", "'line_%s_%s'"%(self.x, self.y))
        return self.js
        
    def build_css(self):
        # default css
        geom_line = {"stroke-width": "1px", "stroke": "black", "fill": None}
        self.css[".geom_line"] = geom_line

        self.css["#line_%s_%s"%(self.x,self.y)] = self.styles
        return self.css

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.name = "bar"
        self._id = 'bar_%s_%s'%(self.x,self.y)
        self.build_js()
        self.build_css()
        self.params = [x,y]
    
    def build_js(self):
        xfxn = JS.Function(None, "d", "return scales.%s_x(d.%s);"%(self.x,self.x)) 
        yfxn = JS.Function(None, "d", "return d.%s_y > 0 ? scales.%s_y(d.%s) : scales.%s_y(0);"%(self.y, self.y, self.y, self.y))
        heightfxn = JS.Function(
            None, 
            "d", 
            "return d.%(y)s > 0 ? scales.%(y)s_y(0) - scales.%(y)s_y(d.%(y)s) : scales.%(y)s_y(d.%(y)s) - scales.%(y)s_y(0);"%{"y":self.y}
        )
        box_width=20

        self.js = JS.JavaScript()
        self.js += JS.Object("g").selectAll("'.bars'") \
                                 .data("data") \
                                 .enter() \
                                 .append("'svg:rect'") \
                                 .attr("'x'", xfxn) \
                                 .attr("'y'", yfxn) \
                                 .attr("'width'", box_width)\
                                 .attr("'height'", heightfxn)
        return self.js
    
    def build_css(self):
        bar = {
            "stroke-width": "1px",
             "stroke": "black",
             "fill-opacity": 0.7,
             "stroke-opacity": 1,
             "fill": "blue"
        }
        self.css[".geom_bar"] = bar 
        # arbitrary styles
        self.css["#"+self._id] = self.styles
        return self.css
        

class Point(Geom):
    def __init__(self,x,y,c=None,**kwargs):
        Geom.__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.c = c
        self._id = 'point_%s_%s_%s'%(self.x,self.y,self.c)
        self.params = [x,y,c]
        self.name = "point"
        self.build_css()
        self.build_js()
    
    def build_css(self):
        point = {
            "stroke-width"  : "1px",
             "stroke"        : "black",
             "fill-opacity"  : 0.7,
             "stroke-opacity": 1,
             "fill"          : "blue"
        }
        self.css[".geom_point"] = point 
        # arbitrary styles
        self.css["#"+self._id] = self.styles
        return self.css
        
    def build_js(self):
        js_cx = JS.Function(None, "d", "return scales.%s_x(d.%s);"%(self.x,self.x)) 
        js_cy = JS.Function(None, "d", "return scales.%s_y(d.%s);"%(self.y,self.y)) 

        obj = JS.Object("g").selectAll("'.geom_point'")      \
                            .data("data")                    \
                            .enter()                         \
                            .append("'svg:circle'")          \
                            .attr("'cx'", js_cx)             \
                            .attr("'cy'", js_cy)             \
                            .attr("'r'", 4)                  \
                            .attr("'class'", "'geom_point'") \
                            .attr("'id'", "'%s'"%self._id)
        if self.c:
            fill = JS.Function(None, "return d.%s;"%self.c)
            obj.add_attribute("style", "fill", fill)
        self.js = JS.JavaScript(obj)
        return self.js
