import threading
import time
import random
from sys import argv
import socket
import numpy as np
clientpk={}
clientconn={}

def client(lsListenPort):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server receive socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    server_binding = ('', lsListenPort)
    ss.bind(server_binding)
    ss.listen(2)
    host = socket.gethostname()
    print("[LS]: LS host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS]: LS IP address is {}".format(localhost_ip))
    try:
        sssen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server send socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    server_binding = ('', 50008)
    sssen.bind(server_binding)
    sssen.listen(2)
    host = socket.gethostname()
    print("[LS]: LS host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS]: LS IP address is {}".format(localhost_ip))

    while True:
        csockid, addr = ss.accept()
        css,addre=sssen.accept()
        clientconn[csockid]=css
        print ("[LS]: Got a connection request from client at {}".format(addr))
        threading.Thread(target=handle_client_in, args=(csockid, addr,css,addre)).start()
    ss.close()


def recvPk(csockid):
    A=np.random.randint(0,1,(8,7))
    b=np.random.rand(8,1)
    i=0
    while i<8:
        j=0
        while j<7:
            num=csockid.recv(1024)
            A[i][j]=num.decode('utf-8')
            csockid.send("yes".encode('utf-8'))
            j=j+1
            pass
        i=i+1
        pass
    i=0
    while i<8:
        num=csockid.recv(1024)
        b[i][0]=float(num.decode('utf-8'))
        csockid.send("yes".encode('utf-8'))
        i=i+1
        pass
    pk=(A,b)
    print(pk)
    clientpk[csockid]=pk
    pass

def sendPk(csr,css):
    allkey=list(clientpk.keys())
    for value in allkey:
        if value!=csr:
            temp=value
            pass
        pass
    A,b=clientpk[temp]
    i=0
    while i<8:
        j=0
        while j<7:
            css.send(str(A[i][j]).encode('utf-8'))
            res=css.recv(1024).decode('utf-8')
            if res!='yes':
                print("error")
                pass
            j=j+1
            pass
        i=i+1
        pass
    i=0
    while i<8:
        css.send(str(b[i][0]).encode('utf-8'))
        res=css.recv(1024).decode('utf-8')
        if res!='yes':
            print("error")
            pass
        i=i+1
        pass
    pass

def revMess(csockid):
    encryList=[]
    corlist=[]
    msg=csockid.recv(1024).decode('utf-8')
    if msg=='sendres':
        while True:
            msg=csockid.recv(1024).decode('utf-8')

            if msg=='end':
                csockid.send('end'.encode('utf-8'))
                break
                pass
            elif msg=='ab':
                encryList.append('ab')
                corlist.append('ab')
                csockid.send('yes'.encode('utf-8'))
            else:
                s=np.random.randint(0,1,(1,7))

                s[0][0]=int(msg)
                st='yes'
                csockid.send(st.encode('utf-8'))
                i=1
                while i<7:
                    msg=csockid.recv(1024).decode('utf-8')

                    s[0][i]=int(msg)
                    csockid.send('yes'.encode('utf-8'))
                    i=i+1
                    pass
                encryList.append(s)
                msg=csockid.recv(1024).decode('utf-8')
                corlist.append(float(msg))
                csockid.send('yes'.encode('utf-8'))
            pass
        print("Message:")
        print(encryList)
        print(corlist)
        return encryList, corlist


def handle_client_in(csockid, addr,css,addre):
    recvPk(csockid)
    while True:
        if len(clientpk)==2:
            sendPk(csockid,css)
            break
            pass
        pass
    while True:
        try:
            encryList, corlist=revMess(csockid)
            brodcast(encryList,corlist, csockid)
        except:
            csockid.close()
            del client[csockid]
        pass

def brodcast(encryList,corlist, csockid):
    for conn in clientconn:
        if conn!=csockid:
            css=clientconn[conn]
            css.send('clientres'.encode('utf-8'))
            res=css.recv(1024).decode('utf-8')
            if res!='start':
                print("error")
                pass
            j=0
            for val in encryList:
                if type(val)==str:
                    if val=='ab':
                        css.send('ab'.encode('utf-8'))
                        res=css.recv(1024).decode('utf-8')
                        if res!='yes':
                            print("error")
                            pass
                        pass
                        j=j+1
                        pass
                else:
                    i=0
                    while i<7:
                        css.send(str(val[0][i]).encode('utf-8'))
                        res=css.recv(1024).decode('utf-8')
                        if res!='yes':
                            print("error")
                            pass
                        i=i+1
                        pass
                    css.send(str(corlist[j]).encode('utf-8'))
                    j=j+1
                    res=css.recv(1024).decode('utf-8')
                    if res!='yes':
                        print("error")
            css.send('end'.encode('utf-8'))
            res=css.recv(1024).decode('utf-8')
            if res!='end':
                print("error")
                pass


if __name__ == "__main__":
    lsListenPort=50007
    client(int(lsListenPort))
    time.sleep(5)
    print("Done.")
