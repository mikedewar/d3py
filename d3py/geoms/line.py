from geom import Geom, JavaScript, Selection, Function

class Line(Geom):
    def __init__(self,x,y,**kwargs):
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.params = [x,y]
        self.debug = True
        self.name = "line"
        self._build_js()
        self._build_css()
        
    def _build_js(self):
        # build scales
        scales = """ 
            scales = {
                x : get_scales(['%s'], 'horizontal'),
                y : get_scales(['%s'], 'vertical')
            }
        """%(self.x, self.y)
        # add the line

        x_fxn = Function(None, "d", "return scales.x(d.%s)"%self.x)
        y_fxn = Function(None, "d", "return scales.y(d.%s)"%self.y)

        draw = Function("draw", ("data", ))
        draw += scales
        draw += "var line = " + Selection("d3.svg").add_attribute("line") \
                                                      .add_attribute("x", x_fxn) \
                                                      .add_attribute("y", y_fxn)

        draw += Selection("g").append("'svg:path'") \
                                 .attr("'d'", "line(data)") \
                                 .attr("'class'", "'geom_line'") \
                                 .attr("'id'", "'line_%s_%s'"%(self.x, self.y))

        self.js = JavaScript(draw)
        return self.js
        
    def _build_css(self):
        # default css
        geom_line = {"stroke-width": "1px", "stroke": "black", "fill": None}
        self.css[".geom_line"] = geom_line

        self.css["#line_%s_%s"%(self.x,self.y)] = self.styles
        return self.css

