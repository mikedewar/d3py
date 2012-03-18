import SimpleHTTPServer

import os
import posixpath
import urllib
import SocketServer

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.seek(0)

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.seek(0)

    def send_head(self):
        """
        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        #path = self.translate_path(self.path)
        path = self.path[1:] #get rid of leading '/'
        f = None
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = self.filemap[path]["fd"]
        except KeyError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", str(f.len))
        self.send_header("Last-Modified", self.date_time_string(self.filemap[path]["timestamp"]))
        self.end_headers()
        return f
