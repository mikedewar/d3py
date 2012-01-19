import SimpleHTTPServer

import os
import posixpath
import urllib
import SocketServer

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def translate_path(self, path):
		"""Translate a /-separated PATH to the local filename syntax.
		
		Components that mean special things to the local file system
		(e.g. drive or directory names) are ignored.  (XXX They should
		probably be diagnosed.)
		
		"""
		# make sure a working directory has been set
		try:
			if not os.path.isdir(self.directory):
				self.directory = os.getcwd()
		except:
			self.directory = os.getcwd()
		# abandon query parameters
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		path = posixpath.normpath(urllib.unquote(path))
		words = path.split('/')
		words = filter(None, words)
		path = self.directory
		for word in words:
			drive, word = os.path.splitdrive(word)
			head, word = os.path.split(word)
			if word in (os.curdir, os.pardir): continue
			path = os.path.join(path, word)
		return path
