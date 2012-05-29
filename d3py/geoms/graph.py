from geom import Geom, JavaScript, Object, Function

class ForceLayout(Geom):
    def __init__(self):
        self.build_js()
    
    def build_js():
        code = """
        // draw the graph nodes
        var node = svg.selectAll("circle.node")
          .data(json.nodes)
          .enter()
          .append("circle")
            .attr("class", "node")
            .attr("r", 12);
            
        // draw the graph edges
        var link = svg.selectAll("line.link")
          .data(json.links)
          .enter().append("line")
            .style('stroke','black');
            
        // create the layout
        var force = d3.layout.force()
            .charge(-120)
            .linkDistance(30)
            .size([width, height])
            .nodes(json.nodes)
            .links(json.links)
            .start();
            
        // define what to do one each tick of the animation
        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
                
            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
            });

        // bind the drag interaction to the nodes
        node.call(force.drag);
        """