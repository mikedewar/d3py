import logging
import webbrowser
from HTTPHandler import CustomHTTPRequestHandler, ThreadedHTTPServer
import IPython.core.display
import threading
from cStringIO import StringIO
import time
import json
import os

from css import CSS
import javascript as JS

class Figure(object):
    def __init__(self, name, width, height, interactive, font, logging,  template, host, port, **kwargs):

        # store data
        self.name = '_'.join(name.split())
        d3py_path = os.path.abspath(os.path.dirname(__file__))
        self.filemap = {
            "static/d3.js":{
                "fd":open(d3py_path+"/d3.js","r"), 
                "timestamp":time.time()
            },
        }

        # Networking stuff
        self.host = host
        self.port = port
        self._server_thread = None
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
        self.template = template or "".join(open(d3py_path+'/d3py_template.html').readlines())
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

    def _build(self):
        logging.debug('building chart')
        self._build_js()
        self._build_css()
        self._build_html()
        self._build_geoms()

    def update(self):
        logging.debug('updating chart')
        self._build()
        self.save()

    def save(self):
        logging.debug('saving chart')
        self._save_data()
        self._save_css()
        self._save_js()
        self._save_html()

    def _clanup(self):
        raise NotImplementedError


    def __enter__(self):
        self.interactive = False
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        if ex_tb is not None:
            print "Cleanup after exception: %s: %s"%(ex_type, ex_value)
        self._cleanup()

    def __del__(self):
        self._cleanup()

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

    def _set_data(self):
        self.update()

    def _add_geom(self, geom):
        self.geoms.append(geom)
        self.save()
    
    def _build_css(self):
        #._build up the basic css
        chart = {}
        chart.update(self.args)
        self.css["#chart"] = chart

    def _build_html(self):
        # we start the html using a template - it's pretty simple
        self.html = self.template
        self.html = self.html.replace("{{ name }}", self.name)
        self.html = self.html.replace("{{ font }}", self.font)
        self._save_html()

    def _build_geoms(self):
        self.js_geoms = JS.JavaScript()
        self.css_geoms = CSS()
        for geom in self.geoms:
            self.js_geoms.merge(geom._build_js())
            self.css_geoms += geom._build_css()

    def __add__(self, geom):
        self._add_geom(geom)

    def __iadd__(self, geom):
        self._add_geom(geom)
        return self

    def _data_to_json(self):
        raise NotImplementedError
        
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

        self.js = JS.JavaScript() + draw + JS.Function("init")

    def _save_data(self,directory=None):
        """
        save a json representation of the figure's data frame
        
        Parameters
        ==========
        directory : str
            specify a directory to store the data in (optional)
        """
        # write data
        filename = "%s.json"%self.name
        self.filemap[filename] = {"fd":StringIO(self._data_to_json()),
                "timestamp":time.time()}

    def _save_css(self):
        # write css
        filename = "%s.css"%self.name
        css = "%s\n%s"%(self.css, self.css_geoms)
        self.filemap[filename] = {"fd":StringIO(css),
                "timestamp":time.time()}

    def _save_js(self):
        # write javascript
        final_js = JS.JavaScript()
        final_js.merge(self.js)
        final_js.merge(self.js_geoms)

        filename = "%s.js"%self.name
        js = "%s"%final_js
        self.filemap[filename] = {"fd":StringIO(js),
                "timestamp":time.time()}

    def _save_html(self):
        # update the html with the correct port number
        self.html = self.html.replace("{{ port }}", str(self.port))
        self.html = self.html.replace("{{ host }}", str(self.host))
        # write html
        filename = "%s.html"%self.name
        self.filemap[filename] = {"fd":StringIO(self.html),
                "timestamp":time.time()}

    def show(self, interactive=None):
        self.update()
        self.save()
        if interactive is not None:
            blocking = not interactive
        else:
            blocking = not self.interactive

        if blocking:
            self._serve(blocking=True)
        else:
            # if not blocking, we serve the 
            self._serve(blocking=False)
            # fire up a browser
            webbrowser.open_new_tab("http://%s:%s/%s.html"%(self.host,self.port, self.name))

    def display(self, width=700, height=400):
        html = "<iframe src=http://%s:%s/%s.html width=%s height=%s>" %(self.host, self.port, self.name, width, height)
        IPython.core.display.HTML(html)

    def _serve(self, blocking=True):
        """
        start up a server to serve the files for this vis.
        """
        msgparams = (self.host, self.port, self.name)
        url = "http://%s:%s/%s.html"%msgparams
        if self._server_thread is None or self._server_thread.active_count() == 0:
            Handler = CustomHTTPRequestHandler
            Handler.filemap = self.filemap
            Handler.logging = self.logging
            try:
                self.httpd = ThreadedHTTPServer(("", self.port), Handler)
            except Exception, e:
                print "Exception %s"%e
                return False
            if blocking:
                logging.info('serving forever on port: %s'%msgparams[1])
                msg = "You can find your chart at " + url
                print msg
                print "Ctrl-C to stop serving the chart and quit!"
                self._server_thread = None
                self.httpd.serve_forever()
            else:
                logging.info('serving asynchronously on port %s'%msgparams[1])
                self._server_thread = threading.Thread(
                    target=self.httpd.serve_forever
                )
                self._server_thread.daemon = True
                self._server_thread.start()
                msg = "You can find your chart at " + url
                print msg


    def _cleanup(self):
        try:
            if self.httpd is not None:
                print "Shutting down httpd"
                self.httpd.shutdown()
                self.httpd.server_close()
        except Exception, e:
            print "Error in clean-up: %s"%e



