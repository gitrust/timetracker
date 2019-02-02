#!c:\Python26\python.exe
# HTTP CGI Server
#

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

serveradress = ("", 8080)
server = HTTPServer(serveradress, CGIHTTPRequestHandler)
print ("HTTP CGI server started at localhost:8080")

server.serve_forever()

