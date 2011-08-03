import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define,options
import os
import json
import logging

class DataHandler(tornado.web.RequestHandler):

    def api_response(self, data, status_code=200, status_txt='OK'):
        """return an api response in the proper output format with status_code == 200"""
        self.set_header("Content-Type", "application/javascript; charset=UTF-8")
        data = json.dumps({'data':data, 'status_code':status_code, 'status_txt':status_txt})
        self.write(data)

    def get(self):
        fh = open('static/temp.json')
        data = json.loads(fh.read())
        fh.close()
        self.api_response(data)

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('ping!')

class LineHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('line.html')

class BarHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('bar.html')

class HistogramHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('histogram.html')

class ScatterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('scatter.html')

application = tornado.web.Application(
    [
        (r"/ping$", PingHandler),
        (r"/line$", LineHandler),
        (r"/bar$", BarHandler),
        (r"/histogram$", HistogramHandler),
        (r"/scatter$", ScatterHandler),
        (r"/data$", DataHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
)

def main():
    define("port", default=7666, help="port num for d3pyplot server", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()