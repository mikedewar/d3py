from css import CSS
import javascript as JS
import templates
import numpy as np

import logging

import webbrowser
from HTTPHandler import CustomHTTPRequestHandler, ThreadedHTTPServer
import threading

import os
import tempfile
import shutil

import json


class D3object(object):

    def build_js():
        raise NotImplementedError

    def build_css():
        raise NotImplementedError

    def build_html():
        raise NotImplementedError

    def build_geoms():
        raise NotImplementedError

    def save_data(self, where=None):
        raise NotImplementedError

    def save_css(self, where=None):
        raise NotImplementedError

    def save_js(self, where=None):
        raise NotImplementedError

    def save_html(self, where=None):
        raise NotImplementedError

    def build(self):
        self.build_js()
        self.build_css()
        self.build_html()
        self.build_geoms()

    def update(self, where=None):
        self.build()
        self.save(where)

    def save(self, where=None):
        if where is not None and not os.path.isdir(where):
            try:
                os.makedirs(where)
            except Exception, e:
                print "Could not create directory structure %s: %s"%(where, e)
        self.save_data(where)
        self.save_css(where)
        self.save_js(where)
        self.save_html(where)

    def clanup(self):
        raise NotImplementedError

    def show(self):
        self.update()
        self.save()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        if ex_tb is not None:
            print "Cleanup after exception: %s: %s"%(ex_type, ex_value)
        self.cleanup()

    def __del__(self):
        self.cleanup()


class Figure(D3object):

    def __init__(self, data, name="figure",
        width=400, height=100, port=8000, template=None, font="Asap", **kwargs):
        """
        data : dataFrame
            data used for the plot. This dataFrame is column centric
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
            
        keyword args are converted from foo_bar to foo-bar if you want to pass
        in arbitrary css to the figure    
        
        """
        # store data
        self.name = name
        self.data = data
        self.work_dir = tempfile.mkdtemp(prefix="d3py-%s"%self.name)
        self.save_data()
        # Networking stuff
        self.port = port
        self.server_thread = None
        self.httpd = None
        self.interactive = False
        # initialise strings
        self.draw = JS.Function("draw", ["data"], "")
        
        # we use bostock's scheme http://bl.ocks.org/1624660
        self.margins = {"top": 10, "right": 20, "bottom": 25, "left": 60}
        self.draw += "var margin = %s;"%json.dumps(self.margins).replace('""','')
        self.draw += "    width = %s - margin.left - margin.right"%width
        self.draw += "    height = %s - margin.top - margin.bottom;"%height
        self.css = CSS()
        self.html = ""
        self.template = template or 'static/d3py_template.html'
        self.js_geoms = ""
        self.css_geoms = CSS()
        self.geoms = []
        # misc arguments - these go into the css!
        self.font = font
        self.args = {
            "width": width - self.margins["left"] - self.margins["right"],
            "height": height - self.margins["top"] - self.margins["bottom"],
            "font-family": "'%s'; sans-serif"%self.font
        }
        kwargs = dict([(k[0].replace('_','-'), k[1]) for k in kwargs.items()])
        self.args.update(kwargs)

    def ion(self):
        """
        Turns interactive mode on ala pylab
        """
        self.interactive = True

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
        create appropriate scales for each column of the data frame
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
                
                y_range = JS.Object("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("range",  height_linspace)
                    
                x_range = JS.Object("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("rangeBands",  [0, width], 0.1)
                    
                scale.update({"%s_y"%colname: str(y_range), "%s_x"%colname: str(x_range)})
            else:
                y_range = JS.Object("d3.scale") \
                    .add_attribute("linear") \
                    .add_attribute("range",  [0, height])
                    
                x_range = JS.Object("d3.scale") \
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
        

    def build_js(self):
        draw_code = JS.JavaScript()
        
        # this approach to laying out the graph is from Bostock: http://bl.ocks.org/1624660
        
        draw_code += "var g = " + JS.Object("d3").select("'#chart'") \
            .append("'svg'") \
            .attr("'width'", 'width + margin.left + margin.right') \
            .attr("'height'", 'height + margin.top + margin.bottom') \
            .append("'g'") \
            .attr("'transform'", "'translate(' + margin.left + ',' + margin.top + ')'")
        
        scale = self.build_scales()
        
        draw_code += "var scales = %s;"%json.dumps(scale, sort_keys=True, indent=4).replace('"', '')

        self.draw += draw_code

    def build_css(self):
        # build up the basic css
        chart = {
        }
        chart.update(self.args)
        self.css["#chart"] = chart

    def build_html(self):
        # we start the html using a template - it's pretty simple
        self.html = templates.d3py_template
        self.html = self.html.replace("{{ name }}", self.name)
        self.html = self.html.replace("{{ font }}", self.font)
        self.save_html()

    def build_geoms(self):
        self.js_geoms = JS.JavaScript()
        self.css_geoms = CSS()
        for geom in self.geoms:
            self.js_geoms += geom.build_js()
            self.css_geoms += geom.build_css()

    def __add__(self, geom):
        self.add_geom(geom)

    def __iadd__(self, geom):
        self.add_geom(geom)
        return self

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

    def save_data(self,directory=None):
        """
        save a json representation of the figure's data frame
        
        Parameters
        ==========
        directory : str
            specify a directory to store the data in (optional)
        """
        # write data
        fname = "%s/%s.json"%(directory or self.work_dir, self.name)
        fh = open(fname, 'w+')
        fh.write(self.data_to_json())
        fh.close()

    def save_css(self, where=None):
        # write css
        fh = open("%s/%s.css"%(where or self.work_dir, self.name), 'w+')
        fh.write("%s\n%s"%(self.css, self.css_geoms))
        fh.close()

    def save_js(self, where=None):
        # write javascript
        fh = open("%s/%s.js"%(where or self.work_dir, self.name), 'w+')
        fh.write("%s"%(self.draw + self.js_geoms))
        fh.close()

    def save_html(self, where=None):
        # update the html with the correct port number
        self.html = self.html.replace("{{ port }}", str(self.port))
        # write html
        fh = open("%s/%s.html"%(where or self.work_dir,self.name),'w+')
        fh.write(self.html)
        fh.close()

    def show(self, interactive=None):
        super(Figure, self).show()

        if interactive is not None:
            blocking = not interactive
        else:
            blocking = not self.interactive

        if blocking:
            self.serve(blocking=True)
        else:
            self.serve(blocking=False)
            # fire up a browser
            webbrowser.open_new_tab("http://localhost:%s/%s.html"%(self.port, self.name))

    def serve(self, blocking=True):
        """
        start up a server to serve the files for this vis.

        """
        if self.server_thread is None or self.server_thread.active_count() == 0:
            Handler = CustomHTTPRequestHandler
            Handler.directory = self.work_dir
            try:
                self.httpd = ThreadedHTTPServer(("", self.port), Handler)
            except Exception, e:
                print "Exception %s"%e
                return False
            if blocking:
                self.server_thread = None
                self.httpd.serve_forever()
            else:
                self.server_thread = threading.Thread(
                    target=self.httpd.serve_forever
                )
                self.server_thread.daemon = True
                self.server_thread.start()
                print "You can find your chart at http://localhost:%s/%s/%s.html"%(self.port, self.name, self.name)

    def cleanup(self):
        try:
            try:
                print "Cleaning temp files"
                shutil.rmtree(self.work_dir)
            except:
                pass
            if self.httpd is not None:
                print "Shutting down httpd"
                self.httpd.shutdown()
                self.httpd.server_close()
        except Exception, e:
            print "Error in clean-up: %s"%e
