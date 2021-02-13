from http.server import HTTPServer, BaseHTTPRequestHandler
from time import strftime
from pathlib import Path
from mimetypes import guess_type

class Server(BaseHTTPRequestHandler):
    """
    Your task is to define this class such that it fulfills the assignment
    requirements.

    Refer to the official Python documentation for the `http.server` class for
    details on what can go in here.

    Replace this pass statement with your own code:
    """




    def do_HEAD(self, statusMessage):
        self.wfile.write(bytes(f"{statusMessage}\n", encoding="utf-8"))
        self.wfile.write(b"Server: The Bestest Server Ever\n")
        self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
        self.wfile.write(b"Cache-Control : max-age=5\n")
        self.wfile.write(b"Connection: close\n")

    def do_GET(self):

        if Path(self.path[1:]).is_file():
            self.do_HEAD("HTTP/1.1 200 OK")
            size = self.get_file_size(self.path[1:])
            self.wfile.write(bytes(f"Content-Type: {guess_type(self.path)[0]}\n", encoding="utf-8"))
            self.wfile.write(bytes(f"Content-Length: {size}\n", encoding="utf-8"))
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file(self.path[1:]))

        elif Path(self.path[1:] + ".html").is_file():
            self.do_HEAD("HTTP/1.1 301 Moved Permanently")
            self.wfile.write(bytes(f"Location : {self.path}.html\n", encoding="utf-8"))
            self.wfile.write(b"\n")

        elif self.path == "/debugging":
            self.do_HEAD("HTTP/1.1 200 OK")
            self.wfile.write(bytes(f"""
                <!DOCTYPE html>
                <html lang='en'>
                    <head>
                        <meta charset='UTF-8'>
                        <link rel='stylesheet' href='style.css' type='text/css'/>
                        <title>Debugging Info</title>
                    </head>
                    <body>
                        <h1 class='heading'>Debugging Page</h1>
                        <ol class='blue'>
                            <li>Server Version: {self.server_version}</li>
                            <li>Server Date: {strftime('%c')}</li>
                            <li>Client IP address: {self.client_address}</li>
                            <li>Path Requested: {self.path}</li>
                            <li>HTTP Request Type: {self.command}</li>
                            <li>HTTP Request Version: {self.request_version}</li>
                            <li>HTTP Headers: <ul>{self.get_html_headers()}</ul></li>
                    </body>
                </html>""", encoding="utf-8"))

        elif "/bio" in self.path:
            self.do_HEAD("HTTP/1.1 301 Moved Permanently")
            self.wfile.write(b"Location: /about.html\n")
            self.wfile.write(b"\n")

        elif self.path == "/help" or self.path == "/tips":
            self.do_HEAD("HTTP/1.1 301 Moved Permanently")
            self.wfile.write(b"Location: /techtips+css.html\n")
            self.wfile.write(b"\n")

        elif self.path == "/":
            self.do_HEAD("HTTP/1.1 301 Moved Permanently")
            self.wfile.write(b"Location: /index.html\n")
            self.wfile.write(b"\n")

        elif self.path == "/forbidden":
            self.do_HEAD("HTTP/1.1 403 Forbidden")
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file("403.html"))

        elif self.path == "/teapot":
            self.do_HEAD("HTTP/1.1 418 I'm a Teapot")
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file("418.html"))

        else:
            self.do_HEAD("HTTP/1.1 404 Not Found")
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file('404.html'))

    def load_file(self, filename):
        # TODO: do some safety checks:
        f = open(filename, "rb")
        data = f.read()
        f.close()
        return data

    def get_file_size(self, filename):
        f = open(filename, "rb")
        data = f.read()
        f.close()
        return len(data)

    def get_html_headers(self):
        header_bytes = ''
        for header, value in self.headers.items():
            header_bytes+=(f'<li>{header} : {value}</li>')

        return header_bytes

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, Server).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)