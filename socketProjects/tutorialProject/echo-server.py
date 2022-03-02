import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def server_func():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        client_host, client_port = sock.accept()
        with client_host:
            print("connected by {}".format(client_port))
            while True:
                data = client_host.recv(1024)
                if not data:
                    break
                client_host.sendall(data)


def main():
    server_func()


main()
