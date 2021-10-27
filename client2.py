import threading
import time
import random
from sys import argv
import socket
import numpy as np
import math
def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C2]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port = 50008
    localhost_addr = socket.gethostbyname(socket.gethostname())

    #open the file
    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    while True:
        # Receive data from the server

        line=input("[C2]:")
        a = np.arange(12).reshape(3,4)
        cs.send(a)
        data_from_server=cs.recv(1024)
        data=data_from_server.decode('utf-8')
        print("[C]: "+data)

    # close

    cs.close()



def keygen():
    n=7
    p=97
    m=8
    B=3
    A=np.random.randint(0,p,(m,n))
    s=np.random.randint(0,p,(n,1))
    e=np.random.rand(m,1)*B
    b=As+e
    return s,(A,b)

def encry(pk,x):
    r=np.random.randint(0,1,(m,1))
    return r.T*A, r.T*b+97*x/2

def decry(sk,ct):
    cf,cs=ct
    x=cs-cf*sk
    if x<97/4:
        return 0
    else:
        return 1

if __name__ == "__main__":
    client()
    time.sleep(5)
    print("Done.")
