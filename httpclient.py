#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Abram Hindle, Devin Dai, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# References:
# https://stackoverflow.com/questions/9530950/parsing-hostname-and-port-from-string-or-url/17769986
# answered Jul 21 '13 at 7:17. Accessed 02-01-2020

# https://docs.python.org/3/library/urllib.parse.html Accessed 02-01-2020

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.splitlines()[0].split(" ")[1]
        code = int(code)
        return code

    def get_headers(self,data):
        headers = data.split('\r\n\r\n')[0]
        return headers

    def get_body(self, data):
        return data.split('\r\n\r\n')[1]
   
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        parsedContent = urlparse(url)
        host = parsedContent.hostname
        port = parsedContent.port
        if port == None:
            port = 80
        self.connect(host, port)
        sendBack = ('GET %s HTTP/1.1\r\nHost: %s \r\nConnection: close\r\n\r\n'%(url, host))
        self.sendall(sendBack)
        response = self.recvall(self.socket)
        self.socket.close()
        print(response)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        parsedContent = urlparse(url)
        host = parsedContent.hostname
        port = parsedContent.port
        if port == None:
            port = 80
        self.connect(host, port)

        body_args = ""
        if args is not None:
            body_args = urlencode(args)

        sendBack = ('POST %s HTTP/1.1\r\nHost: %s \r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length:%s\r\nConnection: close\r\n\r\n%s'%(url, host,len(body_args), body_args))
        self.sendall(sendBack)
        response = self.recvall(self.socket)
        self.socket.close()
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
