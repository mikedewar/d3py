from geom import Geom, JavaScript, Selection, Function

class xAxis(Geom):
    def __init__(self,x, label=None, **kwargs):
        """
        x : string
            name of the column you want to use to define the x-axis
        """
        Geom.__init__(self, **kwargs)
        self.x = x
        self.label = label if label else x
        self.params = [x]
        self._id = 'xaxis'
        self.name = 'xaxis'
        self._build_css()
        self._build_js()
    
    def _build_js(self):
        draw = Function("draw", ("data",), [])
        scale = "scales.x"
        draw += "xAxis = d3.svg.axis().scale(%s)"%scale
        
        xaxis_group = Selection("g").append('"g"') \
              .attr('"class"','"xaxis"') \
              .attr('"transform"', '"translate(0," + height + ")"') \
              .call("xAxis")
        draw += xaxis_group

        if self.label:
            # TODO: Have the transform on this label be less hacky
            label_group = Selection("g").append('"text"') \
                    .add_attribute("text", '"%s"'%self.label) \
                    .attr('"text-anchor"', '"middle"') \
                    .attr('"x"', "width/2") \
                    .attr('"y"', "height+45")
            draw += label_group

        self.js = JavaScript() + draw
        return self.js
    
    def _build_css(self):
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
