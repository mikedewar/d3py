from geom import Geom, JavaScript, Object, Function

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
        draw = Function("draw", ("data", ))

        x_fxn = Function(None, "d", "return scales.%s_x(d.%s)"%(self.x, self.x))
        y_fxn = Function(None, "d", "return scales.%s_y(d.%s)"%(self.y, self.y))

        draw += "var line = " + Object("d3.svg").add_attribute("line") \
                                                      .add_attribute("x", x_fxn) \
                                                      .add_attribute("y", y_fxn)

        draw += Object("g").append("'svg:path'") \
                                 .attr("'d'", "line(data)") \
                                 .attr("'class'", "'geom_line'") \
                                 .attr("'id'", "'line_%s_%s'"%(self.x, self.y))

        self.js = JavaScript(draw)
        return self.js
        
    def build_css(self):
        # default css
        geom_line = {"stroke-width": "1px", "stroke": "black", "fill": None}
        self.css[".geom_line"] = geom_line

        self.css["#line_%s_%s"%(self.x,self.y)] = self.styles
        return self.css

