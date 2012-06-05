from geom import Geom, JavaScript, Selection, Function

class Area(Geom):
    def __init__(self,x,yupper,ylower,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.yupper = yupper
        self.ylower = ylower
        self.params = [x, yupper, ylower]
        self.debug = True
        self.name = "area"
        self.build_js()
        self.build_css()
        
    def build_js(self):
        # add the line
        draw = Function("draw", ("data", ))

        x_fxn = Function(None, "d", "return scales.%s_x(d.%s)"%(self.x, self.x))
        y_fxn = Function(None, "d", "return scales.%s_y(d.%s)"%(self.yupper, self.yupper))
        y0_fxn = Function(None, "d", "return scales.%s_y(d.%s)"%(self.ylower, self.ylower))

        draw += "var area = " + Selection("d3.svg").add_attribute("area") \
            .add_attribute("x", x_fxn) \
            .add_attribute("y0", y0_fxn) \
            .add_attribute("y", y_fxn)

        draw += Selection("g").append("'svg:path'") \
                                 .attr("'d'", "area(data)") \
                                 .attr("'class'", "'geom_area'") \
                                 .attr("'id'", "'area_%s_%s_%s'"%(self.x, self.yupper, self.ylower))

        self.js = JavaScript(draw)
        return self.js
        
    def build_css(self):
        # default css
        geom_line = {"stroke-width": "1px", "stroke": "black", "fill": "blue"}
        self.css[".geom_line"] = geom_line

        self.css["#line_%s_%s_%s"%(self.x,self.yupper, self.ylower)] = self.styles
        return self.css

