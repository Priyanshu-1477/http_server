import socket

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

        first_line = request.split("\n")[0]
        method, path, version = first_line.split(" ")

        if method == "GET":
            if path == "/":
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>Welcome to the Home Page</h1>"
            elif path == "/about":
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>About Us</h1><p>This is a simple web server.</p>"
            else:
                response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<h1>404 Not Found</h1><p>The requested page was not found.</p>"
        else:
            response = "HTTP/1.1 405 Method Not Allowed\nContent-Type: text/html\n\n<h1>405 Method Not Allowed</h1><p>The requested method is not supported.</p>"   

        client_socket.send(response.encode())
        client_socket.close()

start_server()
