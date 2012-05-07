import logging
import webbrowser
from HTTPHandler import CustomHTTPRequestHandler, ThreadedHTTPServer
import threading
from cStringIO import StringIO
import time
import json

from css import CSS
import javascript as JS

class D3object(object):
    
    def build_js():
        raise NotImplementedError

    def build_css():
        raise NotImplementedError

    def build_html():
        raise NotImplementedError

    def build_geoms():
        raise NotImplementedError

    def save_data(self):
        raise NotImplementedError

    def save_css(self):
        raise NotImplementedError

    def save_js(self):
        raise NotImplementedError

    def save_html(self):
        raise NotImplementedError

    def build(self):
        logging.debug('building chart')
        self.build_js()
        self.build_css()
        self.build_html()
        self.build_geoms()

    def update(self):
        logging.debug('updating chart')
        self.build()
        self.save()

    def save(self):
        logging.debug('saving chart')
        self.save_data()
        self.save_css()
        self.save_js()
        self.save_html()

    def clanup(self):
        raise NotImplementedError

    def show(self):
        self.update()
        self.save()

    def __enter__(self):
        self.interactive = False
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        if ex_tb is not None:
            print "Cleanup after exception: %s: %s"%(ex_type, ex_value)
        self.cleanup()

    def __del__(self):
        self.cleanup()

class Figure(D3object):
    def __init__(self, name="figure", width=400, height=100, 
        interactive=True, font="Asap", logging=False,  template=None,
        port=8000, **kwargs):
        # store data
        self.name = '_'.join(name.split())
        self.filemap = {
            "static/d3.js":{
                "fd":open("static/d3.js","r"), 
                "timestamp":time.time()
            },
        }
        # Networking stuff
        self.port = port
        self.server_thread = None
        self.httpd = None
        # interactive is True by default as this is designed to be a command line tool
        # we do not want to block interaction after plotting.
        self.interactive = interactive
        self.logging = logging

        # initialise strings
        self.js = JS.JavaScript()
        self.margins = {
            "top": 10, 
            "right": 20, 
            "bottom": 25, 
            "left": 60, 
            "height":height, 
            "width":width
        }
        
        # we use bostock's scheme http://bl.ocks.org/1624660
        self.css = CSS()
        self.html = ""
        self.template = template or "".join(open('static/d3py_template.html').readlines())
        self.js_geoms = JS.JavaScript()
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
    
    def ioff(self):
        """
        Turns interactive mode off
        """
        self.interactive = False

    def set_data(self):
        self.update()

    def add_geom(self, geom):
        self.geoms.append(geom)
        self.save()
    
    def build_css(self):
        # build up the basic css
        chart = {
        }
        chart.update(self.args)
        self.css["#chart"] = chart

    def build_html(self):
        # we start the html using a template - it's pretty simple
        self.html = self.template
        self.html = self.html.replace("{{ name }}", self.name)
        self.html = self.html.replace("{{ font }}", self.font)
        self.save_html()

    def build_geoms(self):
        self.js_geoms = JS.JavaScript()
        self.css_geoms = CSS()
        for geom in self.geoms:
            self.js_geoms.merge(geom.build_js())
            self.css_geoms += geom.build_css()

    def __add__(self, geom):
        self.add_geom(geom)

    def __iadd__(self, geom):
        self.add_geom(geom)
        return self

    def data_to_json(self):
        raise NotImplementedError
        
    def build_js(self):
        draw = JS.Function("draw", ("data",))
        draw += "var margin = %s;"%json.dumps(self.margins).replace('""','')
        draw += "    width = %s - margin.left - margin.right"%self.margins["width"]
        draw += "    height = %s - margin.top - margin.bottom;"%self.margins["height"]
        # this approach to laying out the graph is from Bostock: http://bl.ocks.org/1624660
        draw += "var g = " + JS.Object("d3").select("'#chart'") \
            .append("'svg'") \
            .attr("'width'", 'width + margin.left + margin.right + 25') \
            .attr("'height'", 'height + margin.top + margin.bottom + 25') \
            .append("'g'") \
            .attr("'transform'", "'translate(' + margin.left + ',' + margin.top + ')'")

        self.js = JS.JavaScript() + draw + JS.Function("init")

    def save_data(self,directory=None):
        """
        save a json representation of the figure's data frame
        
        Parameters
        ==========
        directory : str
            specify a directory to store the data in (optional)
        """
        # write data
        filename = "%s.json"%self.name
        self.filemap[filename] = {"fd":StringIO(self.data_to_json()),
                "timestamp":time.time()}

    def save_css(self):
        # write css
        filename = "%s.css"%self.name
        css = "%s\n%s"%(self.css, self.css_geoms)
        self.filemap[filename] = {"fd":StringIO(css),
                "timestamp":time.time()}

    def save_js(self):
        # write javascript
        final_js = JS.JavaScript()
        final_js.merge(self.js)
        final_js.merge(self.js_geoms)

        filename = "%s.js"%self.name
        js = "%s"%final_js
        self.filemap[filename] = {"fd":StringIO(js),
                "timestamp":time.time()}

    def save_html(self):
        # update the html with the correct port number
        self.html = self.html.replace("{{ port }}", str(self.port))
        # write html
        filename = "%s.html"%self.name
        self.filemap[filename] = {"fd":StringIO(self.html),
                "timestamp":time.time()}

    def show(self, interactive=None):
        super(Figure, self).show()

        if interactive is not None:
            blocking = not interactive
        else:
            blocking = not self.interactive

        if blocking:
            self.serve(blocking=True)
        else:
            # if not blocking, we serve the 
            self.serve(blocking=False)
            # fire up a browser
            webbrowser.open_new_tab("http://localhost:%s/%s.html"%(self.port, self.name))

    def serve(self, blocking=True):
        """
        start up a server to serve the files for this vis.

        """
        msgparams = (self.port, self.name)
        url = "http://localhost:%s/%s.html"%msgparams
        if self.server_thread is None or self.server_thread.active_count() == 0:
            Handler = CustomHTTPRequestHandler
            Handler.filemap = self.filemap
            Handler.logging = self.logging
            try:
                self.httpd = ThreadedHTTPServer(("", self.port), Handler)
            except Exception, e:
                print "Exception %s"%e
                return False
            if blocking:
                logging.info('serving forever on port: %s'%msgparams[0])
                msg = "You can find your chart at " + url
                print msg
                print "Ctrl-C to stop serving the chart and quit!"
                self.server_thread = None
                self.httpd.serve_forever()
            else:
                logging.info('serving asynchronously on port %s'%msgparams[0])
                self.server_thread = threading.Thread(
                    target=self.httpd.serve_forever
                )
                self.server_thread.daemon = True
                self.server_thread.start()
                msg = "You can find your chart at " + url
                print msg


    def cleanup(self):
        try:
            if self.httpd is not None:
                print "Shutting down httpd"
                self.httpd.shutdown()
                self.httpd.server_close()
        except Exception, e:
            print "Error in clean-up: %s"%e



