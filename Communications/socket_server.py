import socket
from threading import Thread
import time
import sys
from settings_ui import dialog
from PyQt5 import QtWidgets
from multiprocessing import Process


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
        self.dq_is_ready = False
        self.da_is_ready = False
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        self.socket_server.bind(self.ADDRESS)
        self.socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        self.client_quit_number = 0

        self.SUBJECT_ID = '0001'
        self.SUBJECT_NAME = 'David'
        self.TRAIN_TIMES = '40'
        self.TEST_SCENE = 'scene1'
        self.TEST_TIMES = '20'
        self.MODE = 'TrainTest'

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

    def show_settings_ui(self):
        app = QtWidgets.QApplication(sys.argv)
        v = dialog.MontageSetDialog()
        v.show()
        sys.exit(app.exec_())

    def message_handle(self, client):
        """
        消息处理
        """
        client.sendall("Hi!".encode(encoding='utf8'))
        while True:
            message = client.recv(1024)
            print("客户端消息:", message.decode())
            # Following Messages may Come From Unity Virtual Scene.
            if message.decode(encoding='utf8') == "vr is on":
                client.sendall(("set_name-" + self.SUBJECT_NAME).encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall(("set_train_times-" + self.TRAIN_TIMES).encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall(("set_test_times-" + self.TEST_TIMES).encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall(("set_scene-" + self.TEST_SCENE).encode(encoding='utf8'))
                time.sleep(0.1)
                client.sendall(("set_mode-" + self.MODE).encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "vr is ready":
                self.vr_is_ready = True
            if message.decode(encoding='utf8') == "LEFTINS":
                self.conn_pool[0].sendall("LEFTINS".encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "RIGHTINS":
                self.conn_pool[0].sendall("RIGHTINS".encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "ENDING":
                self.conn_pool[0].sendall("ENDING".encode(encoding='utf8'))

            # Following Messages may Come From Data Processor.
            if message.decode(encoding='utf8') == "dq is ready":
                self.dq_is_ready = True
                self.conn_pool[0].sendall(("Subject_ID-"+self.SUBJECT_ID).encode(encoding='utf8'))
                time.sleep(0.1)
                self.conn_pool[0].sendall(("Mode-"+self.MODE).encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "LEFT":
                self.conn_pool[1].sendall("res_left".encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "RIGHT":
                self.conn_pool[1].sendall("res_right".encode(encoding='utf8'))

            # Following Messages may Come From Data Acquisition.
            # TODO: Need to Rearrange Connection pool.
            if message.decode(encoding='utf8') == "da is ready":
                self.da_is_ready = True
                self.conn_pool[0].sendall(str(time.time()).encode(encoding='utf8'))
            elif message.decode(encoding='utf8') == "ins_show_settings":
                print("Here is an UI for experiment settings!")
                p = Process(target=self.show_settings_ui)
                p.start()
            elif "inf_name" in message.decode(encoding='utf8'):
                subject_name = message.decode(encoding='utf8')[9:]
                print("Subject Name is " + subject_name)
            elif "inf_id" in message.decode(encoding='utf8'):
                subject_id = message.decode(encoding='utf8')[7:]
                print("Subject ID is " + subject_id)

            if message.decode(encoding='utf8') == "Quit":
                client.close()
                # 删除连接
                self.conn_pool.remove(client)
                print("有一个客户端下线了。")
                self.client_quit_number = self.client_quit_number + 1
                break
