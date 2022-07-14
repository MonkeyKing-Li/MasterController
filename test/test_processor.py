from Communications.socket_server import SocketServer
from threading import Thread

if __name__ == '__main__':
    socket_server = SocketServer()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=socket_server.accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        pass
