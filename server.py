from http.server import HTTPServer, BaseHTTPRequestHandler
from time import strftime

class Server(BaseHTTPRequestHandler):
    """
    Your task is to define this class such that it fulfills the assignment
    requirements.

    Refer to the official Python documentation for the `http.server` class for
    details on what can go in here.

    Replace this pass statement with your own code:
    """


    def get_file_size(self, filename):
        f = open(filename, "rb")
        data = f.read()
        f.close()
        return len(data)

    def do_GET(self):
        imageResourceFiles = {"/images/sad-mondale.jpg", "/images/church.jpg", "/images/gary-hart.jpg", "/images/wendys-burger.jpeg"}
        MAX_AGE = 5
        print(f"The user requested {self.path}")


        if self.path == "/index.html":
            self.wfile.write(b"HTTP/1.1 200 OK\n")
            self.wfile.write(b"Server: Alex T's Server\n")
            self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
            self.wfile.write(bytes(f"Cache-Control : max-age={MAX_AGE}\n", encoding="utf-8"))
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file("index.html"))

        elif self.path == "/style.css":
            self.wfile.write(b"HTTP/1.1 200 OK\n")
            self.wfile.write(b"Server: Alex T's Server\n")
            self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
            size = self.get_file_size("style.css")
            self.wfile.write(b"Content-Type: text/css\n")
            self.wfile.write(bytes(f"Content-Length: {size}\n", encoding="utf-8"))

            self.wfile.write(b"\n")
            self.wfile.write(self.load_file("style.css"))

        elif self.path == "/favicon.ico":
            self.wfile.write(b"HTTP/1.1 200 OK\n")
            self.wfile.write(b"Server: Alex T's Server\n")
            self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
            size = self.get_file_size("style.css")
            self.wfile.write(b"Content-Type: text/css\n")
            self.wfile.write(bytes(f"Content-Length: {size}\n", encoding="utf-8"))
            self.wfile.write(b"\n")
            self.wfile.write(self.load_file('favicon.ico'))

        elif self.path == "/":
            self.wfile.write(b"HTTP/1.1 307 Temporary Redirect\n")
            self.wfile.write(b"Server: Alex T's Server\n")
            self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
            self.wfile.write(b"Location: /index.html\n")
            self.wfile.write(b"\n")

        else:
            self.wfile.write(b"HTTP/1.1 404 Not Found\n")
            self.wfile.write(b"Server: Alex T's Server\n")
            self.wfile.write(bytes(f"Date: {strftime('%c')}\n", encoding="utf-8"))
            self.wfile.write(b"\n")
            # self.wfile.write(self.load_file('404.html'))

    def load_file(self, filename):
        # TODO: do some safety checks:
        f = open(filename, "rb")
       # This slurps the ENTIRE file in all at once; this could cost a lot of RAM with a huge file
        data = f.read()
        f.close()
        return data


if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, Server).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)