from geom import Geom, JavaScript, Object, Function

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
        draw = Function("draw", ("data",))
        js_cx = Function(None, "d", "return scales.%s_x(d.%s);"%(self.x,self.x)) 
        js_cy = Function(None, "d", "return scales.%s_y(d.%s);"%(self.y,self.y)) 

        obj = Object("g").selectAll("'.geom_point'")      \
                            .data("data")                    \
                            .enter()                         \
                            .append("'svg:circle'")          \
                            .attr("'cx'", js_cx)             \
                            .attr("'cy'", js_cy)             \
                            .attr("'r'", 4)                  \
                            .attr("'class'", "'geom_point'") \
                            .attr("'id'", "'%s'"%self._id)
        if self.c:
            fill = Function(None, "return d.%s;"%self.c)
            obj.add_attribute("style", "fill", fill)

        draw += obj
        self.js = JavaScript(draw)
        return self.js
