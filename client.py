import threading
import time
import random
from sys import argv
import socket
import numpy as np
def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    #open the file
    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    while True:
        line=input("[C]:")
        cs.send(line.encode('utf-8'))
        # Receive data from the server
        data_from_server=cs.recv(1024)
        data=data_from_server
        print(data)

    # close

    cs.close()




if __name__ == "__main__":
    client()
    time.sleep(5)
    print("Done.")
