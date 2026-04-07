import socket

def home():
    return serve_file("index.html")

def about():
    return serve_file("about.html")

def serve_file(filename):
    try: 
        with open(filename, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "<h1>404 Not Found</h1><p>The requested file was not found on the server.</p>"

def build_response(body, status):
    return f"""{status}\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}
"""

routes = {
    "/" : home,
    "/about" : about
}
def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("localhost",8080))
    server.listen(5)

    print("Server is listening on http://localhost:8080")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection established with {addr}")
        
        request = client_socket.recv(1024).decode()
        print(f"recieved request: \n{request}")
        try:
            first_line = request.split("\n")[0]
            method, path, version = first_line.split(" ")

        except ValueError:
            client_socket.close()
            continue
    

        if path in routes:
            body = routes[path]()
            status = "HTTP/1.1 200 OK"
        else:
            body = "<h1>404 Not Found</h1><p>The requested page was not found.</p>"
            status = "HTTP/1.1 404 Not Found"

        response = build_response(body, status)

        client_socket.send(response.encode())
        client_socket.close()

start_server()
