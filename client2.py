import threading
import time
import random
from sys import argv
import socket
import numpy as np
import math
import tkinter as tk
import codecs

n=7
p=97
m=8
B=3
pk=()
pkmyself=()
sk=np.random.randint(0,1,(n,1))


def keygen():
    A=np.random.randint(0,p,(m,n))
    s=np.random.randint(0,p,(n,1))
    e=np.random.rand(m,1)*B
    b=np.dot(A, s)+e
    global pkmyself
    pkmyself=(A,b)
    global sk
    sk=s
    return


def encry(pk,x):
    A,b=pk
    r=np.random.randint(0,2,(m,1))

    return np.dot(r.T, A), np.dot(r.T, b)+97*x/2

def decry(ct):
    cf,cs=ct
    x=cs-np.dot(cf,sk)
    if x<97/4:
        return 0
    else:
        return 1

def getMsg(cs):
    while True:
        recvPk(cs)
        if pk!=():
            textMessage.insert('0.0', "Ready to chat")
            print("The other public key:")
            print(pk)
            break
            pass
        pass
    while True:
        try:
            msg=cs.recv(1024).decode('utf-8')
            if msg=='clientres':
                encryList=[]
                corlist=[]
                cs.send('start'.encode('utf-8'))
                while True:
                    msg=cs.recv(1024).decode('utf-8')
                    if msg=='end':
                        cs.send('end'.encode('utf-8'))
                        break
                        pass
                    elif msg=='ab':
                        encryList.append('ab')
                        corlist.append('ab')
                        cs.send('yes'.encode('utf-8'))
                    else:
                        s=np.random.randint(0,1,(1,n))
                        s[0][0]=int(msg)
                        cs.send('yes'.encode('utf-8'))
                        i=1
                        while i<7:
                            msg=cs.recv(1024).decode('utf-8')
                            s[0][i]=int(msg)
                            cs.send('yes'.encode('utf-8'))
                            i=i+1
                            pass
                        encryList.append(s)
                        msg=cs.recv(1024).decode('utf-8')
                        corlist.append(float(msg))
                        cs.send('yes'.encode('utf-8'))
                    pass
                print(corlist)
                print(encryList)
                outlist=[]
                wordseq=()
                i=0
                while i<len(corlist):
                    if corlist[i]=='ab':
                        word= ""
                        outlist.append(word.join(wordseq))
                        wordseq=()
                    else:
                        x=decry((encryList[i],corlist[i]))
                        wordseq=wordseq+(str(x),)
                    i=i+1
                    pass
                sendMessage=''
                for value in outlist:
                    sendMessage=sendMessage+chr(int(value,2))
                    pass
                textMessage.insert('0.0', "[Other]: "+sendMessage)
                pass
        except:
            break
    pass

def sendMess(encryList,corlist,csa):
    csa.send('sendres'.encode('utf-8'))
    j=0
    for val in encryList:
        if type(val)==str:
            if val=='ab':
                csa.send('ab'.encode('utf-8'))
                res=csa.recv(1024).decode('utf-8')
                if res!='yes':
                    print("error")
                    pass
                pass
                j=j+1
                pass
        else:
            i=0
            while i<7:
                csa.send(str(val[0][i]).encode('utf-8'))
                res=csa.recv(1024).decode('utf-8')
                if res!='yes':
                    print("error")
                    pass
                i=i+1
                pass
            csa.send(str(corlist[j][0][0]).encode('utf-8'))
            j=j+1
            res=csa.recv(1024).decode('utf-8')
            if res!='yes':
                print("error")
    csa.send('end'.encode('utf-8'))
    res=csa.recv(1024).decode('utf-8')
    if res!='end':
        print("error")
        pass

def send(csa):
    sendMessage= textText.get('0.0', tk.END)
    messageList=sendMessage.split()
    binList=[]
    for value in sendMessage:
        binList.append(bin(ord(value))[2:])
        pass
    encryList=[]
    corlist=[]
    for value in binList:
        for val in value:
            cf,cs=encry(pk,int(val))
            encryList.append(cf)
            corlist.append(cs)
        encryList.append('ab')
        corlist.append('ab')
        pass
    sendMess(encryList,corlist,csa)
    textText.delete('0.0', tk.END)
    textMessage.insert('0.0', "[Me]: "+sendMessage)


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
    global pk
    pk=(A,b)
    pass


def sendPk(cs):
    A,b=pkmyself
    i=0
    while i<8:
        j=0
        while j<7:
            cs.send(str(A[i][j]).encode('utf-8'))
            res=cs.recv(1024).decode('utf-8')
            if res!='yes':
                print("error")
                pass
            j=j+1
            pass
        i=i+1
        pass
    i=0
    while i<8:
        cs.send(str(b[i][0]).encode('utf-8'))
        res=cs.recv(1024).decode('utf-8')
        if res!='yes':
            print("error")
            pass
        i=i+1
        pass
    pass

if __name__ == "__main__":
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C2]: Client send socket created")
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

    try:
        csr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C2]: Client receive socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    # Define the port on which you want to connect to the server
    port = 50008
    #open the file
    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    csr.connect(server_binding)
    keygen()
    print("My public key:")
    print(pkmyself)
    root=tk.Tk()
    root.title("chat room")
    messageFrame= tk.Frame(width=500, height=300, bg='white')
    textFrame= tk.Frame(width=480, height=100)
    sendFrame= tk.Frame(width=480, height=30)
    textMessage = tk.Text(messageFrame)
    textText = tk.Text(textFrame)
    sendButton = tk.Button(sendFrame, text='send', command=lambda : send(csa=cs))
    messageFrame.grid(row=0, column=0,padx=3, pady=6)
    textFrame.grid(row=1,column=0,padx=3,pady=6)
    sendFrame.grid(row=2,column=0)
    messageFrame.grid_propagate(0)
    textFrame.grid_propagate(0)
    sendFrame.grid_propagate(0)
    textMessage.grid()
    textText.grid()
    sendButton.grid()
    sendPk(cs)
    receiveThread=threading.Thread(target=getMsg, args=(csr,)).start()
    root.mainloop()

    time.sleep(5)
    print("Done.")
