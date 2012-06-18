from geom import Geom, JavaScript, Selection, Function

class ForceLayout(Geom):
    def __init__(self,**kwargs):
        Geom.__init__(self,**kwargs)
        self.name = "forceLayout"
        self._id = 'forceLayout'
        self._build_js()
        self._build_css()
        self.styles = dict([(k[0].replace('_','-'), k[1]) for k in kwargs.items()])
    
    def _build_js(self):
        
        draw = Function("draw", ("data",), [])
        
        draw += Selection("g") \
            .selectAll("'circle.node'") \
            .data("data.nodes") \
            .enter() \
            .append("'circle'") \
            .attr("'class'","'node'") \
            .attr("'r'", 12) 
        
        draw += Selection("g") \
            .selectAll("'line.link'") \
            .data("data.links") \
            .enter() \
            .append("'line'") \
            .attr("'class'", "'link'")
        
        code = [
            "var force = d3.layout.force()",
                ".charge(-120)",
                '.linkDistance(30)',
                '.size([width, height])',
                '.nodes(data.nodes)',
                '.links(data.links);'
               
            
            'force.on("tick", function() {',
                'g.selectAll("line.link").attr("x1", function(d) { return d.source.x; })',
                    '.attr("y1", function(d) { return d.source.y; })',
                    '.attr("x2", function(d) { return d.target.x; })',
                    '.attr("y2", function(d) { return d.target.y; });',
                
                'g.selectAll("circle.node").attr("cx", function(d) { return d.x; })',
                    '.attr("cy", function(d) { return d.y; });',
                '});',
                
            'g.selectAll("circle.node").call(force.drag);',
            
            'force.start();',
        ]
        # TODO the order of the next two lines seems inappropriately important
        draw += JavaScript(code)
        self.js = JavaScript() + draw
        self.js += (Function("init", autocall=True) + "console.debug('Hi');")
        
        return self.js
    
    def _build_css(self):
        line = {
            "stroke-width": "1px",
             "stroke": "black",
        }
        self.css[".link"] = line
        # arbitrary styles
        self.css["#"+self._id] = self.styles
        return self.css
        
