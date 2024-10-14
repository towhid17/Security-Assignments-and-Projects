from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
import AES
import RSA
import time
import os
from pathlib import Path

buffer = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("127.0.0.1", 2022))

def receive():
    while True:
        m = client_socket.recv(buffer).decode()
        data = json.loads(m)
        # print(data)
        fn = data["fn"]
        padsize = data["pad"]
        if fn=="text":
            enkey = RSA.decrypt(data["enkey"])
            # print(enkey)
            orgText = AES.decryptString(data["msg"], enkey)
            orgText = orgText[:-padsize]
            print("new messagee: ", orgText)
            
            dir = os.path.dirname(os.getcwd())
            dir = dir + "\\Don't Open this\\message.txt"

            with open(dir, 'w') as file:
                file.write(orgText)
                file.write('\n')
        
        else:
            namel = fn.split(".")
            fn = namel[0]+"decrypt."+namel[1]
            enkey = RSA.decrypt(data["enkey"])
            # print(enkey)
            entext=""
            entext+=data["msg"]
            iteration = data["iteration"]
            for i in range(iteration):
                mm = client_socket.recv(buffer).decode()
                datam = json.loads(mm)
                entext+=datam["chunk"]
                print(i, "th chunk received")
            
            print("file decryption running .....")
            detext = AES.decryptFile(entext, enkey)
            detext = detext[:-padsize]
            AES.writeFile(fn, detext)
            print("file received!")


def sendmessage(to, msg, enkey, pubkey, fn, padsize):
    m = {"to":to, "msg":msg, "enkey":enkey, "pubkey":pubkey, "fn":fn, "iteration":0, "pad":padsize}
    data = json.dumps(m)
    client_socket.send(data.encode())
    print("sent!")

def sendfile(to, msg, enkey, pubkey, fn, padsize):
    l = len(msg)

    buff = 50
    iteration = int(l//buff)

    chunk = msg[0:buff]

    m = {"to":to, "msg":chunk, "enkey":enkey, "pubkey":pubkey, "fn":fn, "iteration":iteration, "pad":padsize}
    data = json.dumps(m)
    client_socket.send(data.encode())
    time.sleep(1)
    print("0 th chunk sent")

    for i in range(iteration):
        chunk = msg[(i+1)*buff:(i+1)*buff+buff]
        mm = {"to":to, "chunk":chunk}
        datam = json.dumps(mm)
        client_socket.send(datam.encode())
        time.sleep(1)
        print(i+1, "th chunk sent")
    
    print("sent!")

receive_thread = Thread(target=receive)
receive_thread.start()

def sending():
    print("enter name: ")
    name = str(input())
    client_socket.send(name.encode())
    while True:
        print("1. message")
        print("2. file")
        option = int(input())
        if option==1:
            print("to: ")
            to = str(input())

            print("message: ")
            msg = str(input())
            padsize = 16 - len(msg)%16

            print("key: ")
            key = str(input())

            
            msg = AES.encryptString(msg, key)
            enkey, pubkey = RSA.encrypt(key, 32)

            sendmessage(to, msg, enkey, pubkey, "text", padsize)

        elif option==2:
            print("to: ")
            to = str(input())

            print("filename: ")
            fn = str(input())

            file_stats = os.stat(fn)

            padsize = 16- file_stats.st_size%16

            print("key: ")
            key = str(input())

            print("Encryption running.....")
            msg = AES.encryptFile(fn, key)
            enkey, pubkey = RSA.encrypt(key, 32)
            print("Encryption done!")


            # print(msg)

            sendfile(to, msg, enkey, pubkey, fn, padsize)

sendThread = Thread(target=sending)
sendThread.start()