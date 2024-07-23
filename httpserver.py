# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

import threading
def StartHttpServer():      
    t1 = threading.Thread(target=Init)
    t1.start()

def Init():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    #print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    #print("Server stopped.")

def RunPost():
    
    import urllib.request

    url = 
    file_path = r"C:\Users\Eden\Downloads\Lab09\Lab09\Files\file.txt" 

    # with open(file_path, 'rb') as f:
    #     files = {'file': f}
    #     response = requests.post(url, files=files)

    import requests
    response = requests.post('http://httpforever.com/', "hello world")

    # print(response.text)