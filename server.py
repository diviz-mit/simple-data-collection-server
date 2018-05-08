#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

COUNTER = "counter.txt"

def get_querystring(path): 
	pairs = {}
	qstring = path.split('?')
	if len(qstring) == 1: 
		return {} 
	else: 
		qstring = qstring[-1]	
	path = qstring.split('&')
	for pair in path: 
		key, val = pair.split('=')
		pairs[key] = val
	return pairs

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GETTING")
	try:
            if (self.path == '/'): 
                with open(COUNTER, 'r+') as infile: 
                        counter = int(infile.read().strip())
                        infile.seek(0)
                        infile.write(str(counter + 1))
                self._set_headers()
                self.wfile.write(counter)
                return
            elif (self.path == '/reset'): 
                with open(COUNTER, 'w') as outfile: 
                        outfile.write(str(0))
                self._set_headers()
                self.wfile.write(0)
                return
            elif (self.path == '/view'): 
                with open(COUNTER, 'r') as infile: 
                    counter = int(infile.read().strip())
                    self._set_headers()
                    self.wfile.write(counter)
            else: 
                self.send_error(400, "Page does not exist")
	except Exception as e: 
		self.send_error(500, "Internal server error: " + e.message)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
