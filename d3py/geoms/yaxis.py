from geom import Geom, JavaScript, Object, Function

class yAxis(Geom):
    def __init__(self,y, label=None, **kwargs):
        """
        y : string
            name of the column you want to use to define the y-axis
        """
        Geom.__init__(self, **kwargs)
        self.y = y
        self.label = label
        self.params = [y]
        self._id = 'yaxis'
        self.name = 'yaxis'
        self.build_css()
        self.build_js()
    
    def build_js(self):
        draw = Function("draw", ("data",), [])
        scale = "scales.%s_y"%self.y
        draw += "yAxis = d3.svg.axis().scale(%s).orient('left')"%scale
        
        yaxis_group = Object("g").append('"g"') \
              .attr('"class"','"yaxis"') \
              .call("yAxis")
        draw += yaxis_group

        if self.label:
            # TODO: Have the transform on this label be less hacky
            label_group = Object("g").append('"text"') \
                    .add_attribute("text", '"%s"'%self.label) \
                    .attr('"y"', '- margin.left + 15') \
                    .attr('"x"', '- height / 2.0') \
                    .attr('"text-anchor"', '"middle"') \
                    .attr('"transform"', '"rotate(-90, 0, 0)"')
            draw += label_group

        self.js = JavaScript() + draw
        return self.js
    
    def build_css(self):
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".yaxis path"] = axis_path
        axis_path = {
            "fill" : "none",
            "stroke" : "#000"
        }
        self.css[".yaxis line"] = axis_path
        
        return self.css
