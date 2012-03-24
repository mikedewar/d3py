import SimpleHTTPServer
import SocketServer
from cStringIO import StringIO
import sys

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """
        We get rid of the BaseHTTPRequestHandler logging messages
        because they can get annoying!
        """
        if self.logging:
            super().log_message(format, *args)

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
        path = self.path[1:] #get rid of leading '/'
        f = None
        ctype = self.guess_type(path)
        try:
            f = self.filemap[path]["fd"]
        except KeyError:
            return self.list_directory()
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.send_header("Last-Modified", self.date_time_string(self.filemap[path]["timestamp"]))
        self.end_headers()
        return f

    def list_directory(self):
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing</title>\n")
        f.write("<body>\n<h2>Directory listing</h2>\n")
        f.write("<hr>\n<ul>\n")
        for path, meta in self.filemap.iteritems():
            f.write('<li><a href="%s">%s</a>\n' % (path, path))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
