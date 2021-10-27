import threading
import time
import random
from sys import argv
import socket

def client(lsListenPort,ts1ListenPort):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    server_binding = ('', lsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[LS]: LS host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS]: LS IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[LS]: Got a connection request from client at {}".format(addr))
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Client2 socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    server_binding = ('', ts1ListenPort)
    cs.bind(server_binding)
    cs.listen(1)
    csa, addr = cs.accept()
    print ("[LS]: Got a connection request from client at {}".format(addr))

    while True:
        data_from_client=csockid.recv(1024)
        data_from_c2=csa.recv(1024)
        data=data_from_client.decode('utf-8')
        print("[C]: "+data)
        csa.send(data_from_client)
        data=data_from_c2
        print("[C2]: "+data)
        csockid.send(data_from_client)


    ss.close()




if __name__ == "__main__":
    lsListenPort=50007
    ts1ListenPort=50008
    client(int(lsListenPort), int(ts1ListenPort))
    time.sleep(5)
    print("Done.")
