from geom import Geom, JavaScript, Object

class xAxis(Geom):
    def __init__(self,x, **kwargs):
        """
        x : string
            name of the column you want to use to define the x-axis
        """
        Geom.__init__(self, **kwargs)
        self.x = x
        self.params = [x]
        self._id = 'xaxis'
        self.name = 'xaxis'
        self.build_css()
        self.build_js()
    
    def build_js(self):
        scale = "scales.%s_x"%self.x
        self.js = JavaScript()
        self.js += "xAxis = d3.svg.axis().scale(%s)"%scale
        
        xaxis_group = Object("g").append('"g"') \
              .attr('"class"','"xaxis"') \
              .attr('"transform"', '"translate(0," + height + ")"') \
              .call("xAxis")
        self.js += xaxis_group
        return self.js
    
    def build_css(self):
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".xaxis path"] = axis_path
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".xaxis line"] = axis_path
        
        return self.css
