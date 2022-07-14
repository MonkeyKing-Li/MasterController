import socket
from threading import Thread
import time


class SocketServer:
    def __init__(self):
        """
        初始化服务端
        """
        self.ADDRESS = ('127.0.0.1', 6666)
        # self.ADDRESS = ('192.168.1.101', 6666)
        self.socket_server = None
        self.conn_pool = []
        self.vr_is_ready = False
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        self.socket_server.bind(self.ADDRESS)
        self.socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        print("服务端已启动，等待客户端连接...")

    def accept_client(self):
        """
        接收新连接
        """
        while True:
            client, _ = self.socket_server.accept()  # 阻塞，等待客户端连接
            # 加入连接池
            self.conn_pool.append(client)
            # 给每个客户端创建一个独立的线程进行管理
            client_thread = Thread(target=self.message_handle, args=(client,))
            # 设置成守护线程
            client_thread.setDaemon(True)
            client_thread.start()

    def message_handle(self, client):
        """
        消息处理
        """
        client.sendall("Hi!".encode(encoding='utf8'))
        while True:
            message = client.recv(1024)
            print("客户端消息:", message.decode())
            if message.decode(encoding='utf8') == "vr is on":
                client.sendall("set_name-Bob".encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall("set_times-20".encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall("set_scene-scene1".encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall("set_mode-both".encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "vr is ready":
                self.vr_is_ready = True
            if message.decode(encoding='utf8') == "Quit":
                client.close()
                # 删除连接
                self.conn_pool.remove(client)
                print("有一个客户端下线了。")
                break
