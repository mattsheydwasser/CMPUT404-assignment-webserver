#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8').strip()
        
        # print the recieved request and split the data into a list 
        print ("Got a request of: %s\n" % self.data)
        data_list = []
        if self.data != '':
            data_list = (self.data).split(' ')


        # only allows for GET requests to be made
        if data_list[0] != 'GET':
            header = 'HTTP/1.1 405 Not Found\n\n'
            response = '<html><title>Error 405: Not Found</title></html>'
            header += response
            self.request.sendall((header.encode('utf-8')))
        

        # makes sure users cannot backtrack inside directories
        if '/../' in data_list[1]:
            header = 'HTTP/1.1 404 Page Not Found\n\n'
            response = '<html><title>Error 404: Page Not Found</title></html>'
            header += response
            self.request.sendall((header.encode('utf-8')))


        # gets the requested file from the header
        get_file = data_list[1]
        get_file = get_file.lstrip('/')
        

        # redirections for empty ending of deep and hardcore directories
        if get_file == 'deep':
            #get_file = '/index.html'
            red_header = 'HTTP/1.1 301 Moved Permanently \n'
            location = f'Location: deep/\n\n'
            red_header  += location

            self.request.sendall(red_header.encode('utf-8'))
            return
        if get_file == 'hardcore':
            #get_file = '/index.html'
            red_header = 'HTTP/1.1 301 Moved Permanently \n'
            location = f'Location: hardcore/\n\n'
            test += location

            self.request.sendall(red_header.encode('utf-8'))
            return

            
        # set the wanted file according to the requested page, home index.html if blank
        if get_file == 'deep/':
            get_file = 'deep/index.html'
        elif get_file == 'hardcode/':
            get_file = 'hardcode/index.html'
        elif get_file == '':
            get_file = 'index.html'        


        # read from the file that was requested, input the correct mimetype, header, and response
        # if page not found, give 404 error
        try: 
            file = open(f'www/{get_file}', 'rb')
            response = file.read()
            file.close()
            header += 'HTTP/1.1 200 OK \n'
            
            if (get_file.endswith('.css')):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: '+str(mimetype)+'\n\n'

        except Exception as exception:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = f'<html><title>Error 404: Page Not Found {get_file}</title></html>'.encode('utf-8')


      
        final = header.encode('utf-8')
        final += response

        print(final)
        self.request.sendall(final)
        self.request.sendall(bytearray("OK",'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
