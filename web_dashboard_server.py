from http.server import SimpleHTTPRequestHandler, HTTPServer

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard':
            try:
                with open('index.html', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "Dashboard file not found")
        elif self.path in ['/gas_val.txt', '/temp_val.txt', '/ldr_val.txt']:
            try:
                with open(self.path.lstrip('/'), 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

if __name__ == '__main__':
    port = 5000  # Change this if needed
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f'Server running at http://localhost:{port}')
    print(f'Dashboard available at: http://localhost:{port}/dashboard')
    httpd.serve_forever()
