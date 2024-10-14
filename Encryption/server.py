from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
import time

sockets = {}
buffer = 1024
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("127.0.0.1", 2022))


def AcceptUserConnection():
    while True:
        c, addr = server_socket.accept()
        Thread(target=ClientThread, args=(c, addr)).start()


def ClientThread(c, addr):
    name = c.recv(buffer).decode("utf8")
    sockets[name] = c
    print("%s connected" % name)
    while True:
        m = c.recv(buffer)
        data = json.loads(m.decode())
        to = data["to"]
        sockets[to].send(m)
        time.sleep(1)
        

if __name__ == "__main__":
    server_socket.listen(5)
    print("Running...")
    x = Thread(target=AcceptUserConnection)
    x.start()
    x.join()
    server_socket.close()
