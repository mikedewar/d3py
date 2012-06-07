import numpy as np
import logging
import json

import javascript as JS
from d3py import Figure

class PandasFigure(Figure):
    def __init__(self, data, name="figure", width=400, height=100, 
        interactive=True, font="Asap", logging=False,  template=None,
        port=8000, **kwargs):
        """
        data : dataFrame
            pandas dataFrame used for the plot. This dataFrame is column centric
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
        
        """
        super(PandasFigure, self).__init__(
            name=name, width=width, height=height, 
            interactive=interactive, font=font, logging=logging,  template=template,
            port=port, **kwargs
        )
        # store data
        self.data = data
        self.save_data()

    def set_data(self, data):
        errmsg = "the %s geom requests %s which is not the given dataFrame!"
        for geom in self.geoms:
            for param in geom.params:
                if param:
                    assert param in data, errmsg%(geom.name, param)
        self.update()

    def add_geom(self, geom):
        errmsg = "the %s geom requests %s which is not in our dataFrame!"
        for p in geom.params:
            if p:
                assert p in self.data, errmsg%(geom.name, p)
        self.geoms.append(geom)
        self.save()

    def build_scales(self):
        """
        build a function that returns the requested scale 
        """
        logging.debug('building scales')
        get_scales = JS.Function("get_scales", ("colnames", "orientation"))
                           
        get_scales += "console.log('what up')"
        get_scales += "scale = d3.scale.linear()"
        get_scales += "return scale"
        return get_scales

        """
        # we take a slightly over the top approach to scales at the moment
        scale = {}
        width = self.args["width"]
        height = self.args["height"]
        for colname in self.data.columns:
            # we test to see if the column contains strings or numbers
            if type(self.data[colname][0]) is str:
                logging.info("using ordinal scale for %s"%colname)
                # if the column contains characters, build an ordinal scale
                height_linspace = np.linspace(height,0,len(self.data[colname]))
                height_linspace = [int(h) for h in height_linspace]
                
                width_linspace = np.linspace(0, width,len(self.data[colname]))
                width_linspace = [int(w) for w in width_linspace]
                
                y_range = JS.Selection("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("range",  height_linspace)
                    
                x_range = JS.Selection("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("rangeBands",  [0, width], 0.1)
                    
                scale.update({"%s_y"%colname: str(y_range), "%s_x"%colname: str(x_range)})
            else:
                y_range = JS.Selection("d3.scale") \
                    .add_attribute("linear") \
                    .add_attribute("range",  [0, height])
                    
                x_range = JS.Selection("d3.scale") \
                    .add_attribute("linear")\
                    .add_attribute("range",  [0, width])
                
                if min(self.data[colname]) < 0:
                    x_range.add_attribute("domain", [min(self.data[colname]), max(self.data[colname])])
                    y_range.add_attribute("domain", [max(self.data[colname]), min(self.data[colname])])
                else:
                    x_range.add_attribute("domain", [0, max(self.data[colname])])
                    y_range.add_attribute("domain", [max(self.data[colname]), 0])
                    
                scale.update({"%s_y"%colname: str(y_range), "%s_x"%colname: str(x_range)})
        return scale
        """        

    def build_js(self):
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
        
        draw += self.build_scales()
        self.js = JS.JavaScript() + draw + JS.Function("init")

    def data_to_json(self):
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
