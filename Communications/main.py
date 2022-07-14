from Communications.socket_server import SocketServer
from threading import Thread
import time
import random
import subprocess


def my_popen(m_cmd):
    proc = subprocess.Popen(m_cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    return proc.stdout.read().decode()


def exe_open():
    my_popen("D:/Software_Work/Hand_Release/hand.exe")


if __name__ == '__main__':
    exe_thread = Thread(target=exe_open)
    exe_thread.setDaemon(True)
    exe_thread.start()
    rightTimes = 0
    leftTimes = 0
    socket_server = SocketServer()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=socket_server.accept_client)
    thread.setDaemon(True)
    thread.start()
    while not socket_server.vr_is_ready:
        pass
    time.sleep(3)
    for i in range(40):
        if random.randint(0, 1) and rightTimes <= 19 or leftTimes >= 20:
            rightTimes = rightTimes + 1
            time.sleep(1)
            socket_server.conn_pool[0].sendall("ins_ready".encode(encoding='utf8'))
            time.sleep(5)
            socket_server.conn_pool[0].sendall("ins_right".encode(encoding='utf8'))
            time.sleep(7)
            socket_server.conn_pool[0].sendall("ins_rest_correct".encode(encoding='utf8'))
            time.sleep(5)
        else:
            leftTimes = leftTimes + 1
            time.sleep(1)
            socket_server.conn_pool[0].sendall("ins_ready".encode(encoding='utf8'))
            time.sleep(5)
            socket_server.conn_pool[0].sendall("ins_left".encode(encoding='utf8'))
            time.sleep(7)
            socket_server.conn_pool[0].sendall("ins_rest_correct".encode(encoding='utf8'))
            time.sleep(5)
    time.sleep(1)
    socket_server.conn_pool[0].sendall("ins_end".encode(encoding='utf8'))
    # while True:
    # pass
