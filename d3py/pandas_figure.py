import numpy as np
import logging
import json

import javascript as JS
from figure import Figure

class PandasFigure(Figure):
    def __init__(self, data, name="figure", width=800, height=400, 
        columns = None, use_index=False, interactive=True, font="Asap", 
        logging=False,  template=None, host="localhost", port=8000, **kwargs):
        """
        data : dataFrame
            pandas dataFrame used for the plot. This dataFrame is column centric
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
        width : int 
            width of the figure in pixels (default is 1024)
        height : int 
            height of the figure in pixels (default is 768)
        columns: dict, default None
            DataFrame columns you want to visualize for Vega 
        use_index: boolean, default False
            If true, D3py.Vega uses the index for the x-axis instead of a second
            column
        interactive : boolean
            set this to false if you are drawing the graph using a script and
            not in the command line (default is True)
        font : string
            name of the font you'd like to use. See     
            http://www.google.com/webfonts for options (default is Asap)
            
        keyword args are converted from foo_bar to foo-bar if you want to pass
        in arbitrary css to the figure    
        
        """
        super(PandasFigure, self).__init__(name=name, width=width, height=height, 
                                           interactive=interactive, font=font, 
                                           logging=logging,  template=template,
                                           host=host, port=port, **kwargs)
    
        # store data
        self.columns = columns
        self.use_index = use_index
        self.data = data
        self._save_data()

    def _set_data(self, data):
        errmsg = "the %s geom requests %s which is not the given dataFrame!"
        for geom in self.geoms:
            for param in geom.params:
                if param:
                    assert param in data, errmsg%(geom.name, param)
        self.update()

    def _add_geom(self, geom):
        errmsg = "the %s geom requests %s which is not in our dataFrame!"
        for p in geom.params:
            if p:
                assert p in self.data, errmsg%(geom.name, p)
        self.geoms.append(geom)
        self.save()

    def _build_scales(self):
        """
        build a function that returns the requested scale 
        """
        logging.debug('building scales')
        get_scales = """
        function get_scales(colnames, orientation){
            var this_data = d3.merge(
                colnames.map(
                    function(name){
                        return data.map(
                            function(d){
                                return d[name]
                            }
                        )
                    }
                )
            )
            if (orientation==="vertical"){
                if (isNaN(this_data[0])){
                    // not a number
                    console.log('using ordinal scale for vertical axis')
                    scale = d3.scale.ordinal()
                        .domain(this_data)
                        .range(d3.range(height,0,height/this_data.length))
                } else {
                    // a number
                    console.log('using linear scale for vertical axis')
                    extent = d3.extent(this_data)
                    extent[0] = extent[0] > 0 ? 0 : extent[0]
                    scale = d3.scale.linear()
                        .domain(extent)
                        .range([height,0])

                }
            } else {
                if (isNaN(this_data[0])){
                    // not a number
                    console.log('using ordinal scale for horizontal axis')
                    scale = d3.scale.ordinal()
                        .domain(this_data)
                        .rangeBands([0,width], 0.1)
                } else {
                    // a number
                    console.log('using linear scale for horizontal axis')
                    scale = d3.scale.linear()
                        .domain(d3.extent(this_data))
                        .range([0,width])
                }
            }
            return scale
        }
        """
        return get_scales

    def _build_js(self):
        draw = JS.Function("draw", ("data",))
        draw += "var margin = %s;"%json.dumps(self.margins).replace('""','')
        draw += "    width = %s - margin.left - margin.right"%self.margins["width"]
        draw += "    height = %s - margin.top - margin.bottom;"%self.margins["height"]
        # this approach to laying out the graph is from Bostock: http://bl.ocks.org/1624660
        draw += "var g = " + JS.Selection("d3").select("'#chart'") \
            .append("'svg'") \
            .attr("'width'", 'width + margin.left + margin.right + 25') \
            .attr("'height'", 'height + margin.top + margin.bottom + 25') \
            .append("'g'") \
            .attr("'transform'", "'translate(' + margin.left + ',' + margin.top + ')'")
        scales = self._build_scales()
        draw += scales
        self.js = JS.JavaScript() + draw + JS.Function("init")

    def _data_to_json(self):
        """
        converts the data frame stored in the figure to JSON
        """
        def cast(a):
            try:
                return float(a)
            except ValueError:
                return a

        d = [
            dict([
                (colname, cast(row[i]))
                for i,colname in enumerate(self.data.columns)
            ])
            for row in self.data.values
        ]
        try:
            s = json.dumps(d, sort_keys=True, indent=4)
        except OverflowError, e:
            print "Error: Overflow on variable (type %s): %s: %s"%(type(d), d, e)
            raise
        return s
