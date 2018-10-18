import socketserver, socket, sys


host = "0.0.0.0"
port = 10000
address = (host, port)

# this is a sub-class which flips this single parameter to True
class MyTCPServer(socketserver.TCPServer):
    # from https://docs.python.org/3/library/socketserver.html#socketserver.BaseServer.allow_reuse_address
    allow_reuse_address = True


# this is running a socket server in python
class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        message = self.request.recv(10).strip()
        print(f"Got a  message: {message}")

        if message == b"ping":
            self.request.sendall(b"pong\n")


# lets make some code that can run this handler above
def serve():
    server = MyTCPServer(address, TCPHandler)
    server.serve_forever()

def ping():
    # create a IP (AF_INET), TCP (SOCK_STREAM) type socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(b"ping")
    data = sock.recv(10)
    print(f"Recieved {data.decode()}")


# define a way to call serve when someone runs the file
# this lets python know the user is running from the command line
# and not just importing it somewhere else.
if __name__ == "__main__":
    # argv from sys takes command line arguments into program for parsing
    command = sys.argv[1]
    if command == "serve":
        serve()
    elif command == "ping":
        ping()
    else:
        print("invalid command")