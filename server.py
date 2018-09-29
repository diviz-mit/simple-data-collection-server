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
import os
import shutil
import json
from urllib.parse import parse_qs
from save_data import save_locally, save_s3

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

    def _copyfile(self, source, dest): 
        shutil.copyfileobj(source, dest);

    def do_GET(self):
        print("GETTING")
        self._set_headers()
        try:
            if (self.path == '/'): 
                # show the main html stuff
                index_path = "html/index.html"
                try: 
                    f = open(index_path, 'rb')
                except IOError: 
                    self.send_error(404, "File not found")
                    return;
                self._copyfile(f, self.wfile)
                f.close() 
                return;
            elif (self.path == '/counter'): 
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
            if (self.path == "/data"): 
                self._set_headers()
                assert self.headers['Content-type'] == 'application/x-www-form-urlencoded'
                data = self.rfile.read(int(self.headers['Content-Length']))
                data = data.decode("utf-8")
                data = parse_qs(data)
                print("DATA", data)
                #filename = save_locally('output', data)
                save_s3('output', data)
                #print("GOT DATA: saved to file %s", filename)
                print("GOT DATA")
                print(data)
                self.send_response(200)
            else: 
                self.send_error(400, "Page does not exist")
        except Exception as e: 
            self.send_error(500, "Internal server error: " + e.message)

        
def run(server_class=HTTPServer, handler_class=S, port=8000):
    # if we are on heroku, set the port according to heroku's instructions 
    ON_HEROKU = os.environ.get('ON_HEROKU', False)    
    #print("ON_HEROKU", ON_HEROKU)
    if ON_HEROKU: 
        port = int(os.environ.get('PORT'))
        print("Found port via Heroku: %d", port)

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
