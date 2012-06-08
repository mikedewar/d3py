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


        scales = """
            scales = {
                x: get_scales(['%s'], 'horizontal'),
                y: get_scales(['%s','%s'], 'vertical')
            }
        """%(self.x, self.ylower, self.yupper)


        x_fxn = Function(None, "d", "return scales.x(d.%s)"%self.x)
        y1_fxn = Function(None, "d", "return scales.y(d.%s)"%self.yupper)
        y0_fxn = Function(None, "d", "return scales.y(d.%s)"%self.ylower)


        draw = Function("draw", ("data", ))
        draw += scales
        draw += "var area = " + Selection("d3.svg").add_attribute("area") \
            .add_attribute("x", x_fxn) \
            .add_attribute("y0", y0_fxn) \
            .add_attribute("y1", y1_fxn)
    
        draw += "console.log(data)"
        draw += "console.log(area(data))"
        draw += "console.log(scales.y(data[0].y))"
        
        draw += Selection("g").append("'svg:path'") \
             .attr("'d'", "area(data)") \
             .attr("'class'", "'geom_area'") \
             .attr("'id'", "'area_%s_%s_%s'"%(self.x, self.yupper, self.ylower))

        self.js = JavaScript(draw)
        return self.js
        
    def build_css(self):
        # default css
        geom_area = {"stroke-width": "1px", "stroke": "black", "fill": "MediumSeaGreen"}
        self.css[".geom_area"] = geom_area

        self.css["#area_%s_%s_%s"%(self.x,self.yupper, self.ylower)] = self.styles
        return self.css

