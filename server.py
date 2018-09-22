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
from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback

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
        self._set_headers()
        try:
            if (self.path == '/'): 
                with open(COUNTER, 'r+') as infile: 
                        counter = int(infile.read().strip())
                        infile.seek(0)
                        infile.write(str(counter + 1))
                self.wfile.write(str(counter).encode())
                return
            elif (self.path == '/reset'): 
                with open(COUNTER, 'w') as outfile: 
                        outfile.write(str(0))
                self.wfile.write(str(0).encode())
                return
            elif (self.path == '/view'): 
                with open(COUNTER, 'r') as infile: 
                    counter = int(infile.read().strip())
                    self.wfile.write(str(counter).encode())
            else: 
                self.send_error(400, "Page does not exist")
        except Exception as e: 
            #print(e)
            traceback.print_exc()
            self.send_error(500, "Internal server error: {}".format(e))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # When it receives a POST request, it parses the data as json and creates a new file 
        # to save the data. 
        # the file name is fixed for rn. 
        try: 
            if (self.path == "/"): 
                self._set_headers()
                data = self.rfile.read(int(self.headers['Content-Length']))
                data = json.loads(data)
                with open("output.json", "w") as outfile: 
                    json.dump(data, outfile)
                print("GOT DATA")
                print(data)
                self.send_response(200)
            else: 
                self.send_error(400, "Page does not exist")
        except Exception as e: 
            self.send_error(500, "Internal server error: " + e.message)

        
def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
