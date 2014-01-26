import logging
import json
from networkx.readwrite import json_graph

import javascript as JS
from figure import Figure

class NetworkXFigure(Figure):
    def __init__(self, graph, name="figure", width=400, height=100, 
        interactive=True, font="Asap", logging=False,  template=None,
        host="localhost", port=8000, **kwargs):
        """
        data : networkx gprah
            networkx graph used for the plot.
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
        width : int 
            width of the figure in pixels (default is 400)
        height : int 
            height of the figure in pixels (default is 100)
        interactive : boolean
            set this to false if you are drawing the graph using a script and
            not in the command line (default is True)
        font : string
            name of the font you'd like to use. See     
            http://www.google.com/webfonts for options (default is Asap)
            
        keyword args are converted from foo_bar to foo-bar if you want to pass
        in arbitrary css to the figure    
        
        You will need NetworkX installed for this type of Figure to work!
        http://networkx.lanl.gov/
        """
        super(NetworkXFigure, self).__init__(
            name=name, width=width, height=height, 
            interactive=interactive, font=font, logging=logging,  template=template,
            host=host, port=port, **kwargs
        )
        # store data
        self.G = graph
        self._save_data()

    def _data_to_json(self):
        """
        converts the data frame stored in the figure to JSON
        """
        data = json_graph.node_link_data(self.G)
        s = json.dumps(data)
        return s
