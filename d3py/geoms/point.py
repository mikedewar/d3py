from geom import Geom, JavaScript, Selection, Function

class Point(Geom):
    def __init__(self,x,y,c=None,**kwargs):
        Geom.__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.c = c
        self._id = 'point_%s_%s_%s'%(self.x,self.y,self.c)
        self.params = [x,y,c]
        self.name = "point"
        self._build_css()
        self._build_js()
    
    def _build_css(self):
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
        
    def _build_js(self):
        scales = """ 
            scales = {
                x : get_scales(['%s'], 'horizontal'),
                y : get_scales(['%s'], 'vertical')
            }
        """%(self.x, self.y)
        draw = Function("draw", ("data",))
        draw += scales
        js_cx = Function(None, "d", "return scales.x(d.%s);"%self.x) 
        js_cy = Function(None, "d", "return scales.y(d.%s);"%self.y) 

        obj = Selection("g").selectAll("'.geom_point'")      \
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
