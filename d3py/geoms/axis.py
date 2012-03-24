from geom import Geom, JavaScript, Object, Function

class Axis(Geom):
    def __init__(self, var, orient=None, **kwargs):
        """
        var : string
            name of the column you want to use to define the axis
        """
        Geom.__init__(self, **kwargs)
        self.var = var
        self.orient = orient
        self.params = [var]
        self._id = '%s_axis'%var
        self.name = '%s_axis'%var
        self.build_css()
        self.build_js()
    
    def build_js(self):
        draw = Function("draw", ("data",), [])
        scale = "scales.%s_%s"%(self.var, self.var)
        draw += "%s = d3.svg.axis().scale(%s)%s"%(self.name, scale, ".orient('%s')"%self.orient if self.orient else "")
        
        axis_group = Object("g").append('"g"') \
              .attr('"class"','"%s"'%self.name) \
              .attr('"transform"', '"translate(" + margin + ",0)"') \
              .call(self.name)
        draw += axis_group

        self.js = JavaScript() + draw
        return self.js
    
    def build_css(self):
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".%s path"%self.name] = axis_path
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".%s line"%self.name] = axis_path
        
        return self.css
