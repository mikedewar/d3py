from geom import Geom, JavaScript, Object, Function

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        """
        This is a vertical bar chart - the height of each bar represents the 
        magnitude of each class
        
        x : string
            name of the column that contains the class labels
        y : string
            name of the column that contains the magnitude of each class
        """
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.name = "bar"
        self._id = 'bar_%s_%s'%(self.x,self.y)
        self.build_js()
        self.build_css()
        self.params = [x,y]
        self.styles = dict([(k[0].replace('_','-'), k[1]) for k in kwargs.items()])
    
    def build_js(self):
        xfxn = Function(None, "d", "return scales.%s_x(d.%s);"%(self.x,self.x)) 
        
        yfxn = Function(
            None,
            "d",
            "return scales.%(y)s_y(d.%(y)s)"%{"y":self.y}
        )
        
        heightfxn = Function(
            None, 
            "d", 
            "return height - scales.%(y)s_y(d.%(y)s)"%{"y":self.y}
        )

        draw = Function("draw", ("data",), [])
        draw += Object("g").selectAll("'.bars'") \
            .data("data") \
            .enter() \
            .append("'rect'") \
            .attr("'class'", "'geom_bar'") \
            .attr("'id'", "'%s'"%self._id) \
            .attr("'x'", xfxn) \
            .attr("'y'", yfxn) \
            .attr("'width'", "scales.%s_x.rangeBand()"%self.x)\
            .attr("'height'", heightfxn)
        # TODO: rangeBand above breaks for histogram type bar-plots... fix!

        self.js = JavaScript() + draw
        self.js += (Function("init", autocall=True) + "console.debug('Hi');")
        return self.js
    
    def build_css(self):
        bar = {
            "stroke-width": "1px",
             "stroke": "black",
             "fill-opacity": 0.7,
             "stroke-opacity": 1,
             "fill": "blue"
        }
        bar.update
        self.css[".geom_bar"] = bar 
        # arbitrary styles
        self.css["#"+self._id] = self.styles
        return self.css
