import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def client_func():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        for i in range(10):
            send_str = "Hello world {}".format(i)
            sock.sendall(bytes(send_str, "ascii"))
            data = sock.recv(1024)
            print("Received {}!".format(repr(data)))


def main():
    client_func()


main()
