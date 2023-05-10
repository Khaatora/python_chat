import socket
import threading
import hashlib

host = '127.0.0.1'
port = 50000
#Default name
name = "Anonymous"


def first(name, host, port):
    print ("hi ", name, "\n"
           "Current set host :", host, "\n"
           "Current set port :", port, "\n\n"
           "Enter 1 to change your name \n"
           "Enter 2 to change host and port \n"
           "Enter 3 to join chat room \n"
           "Enter exit at any time to close the chat \n"
           )
    #variable to check what the Client wants to do
    control = str(input())
    if control == "1":
        changeName(host, port)
    elif control == "2":
        changeHostPort(name)
    elif control == "3":
        connecting(name, host, port)
    elif control == "exit":
        return
    else:
        first(name, host, port)


def changeName(host, port):
    name = str(input("name : "))
    first(name, host, port)


def changeHostPort(name):
    host = str(input("host : "))
    port = int(input("port : "))
    first(name, host, port)

#connect to server and start threads
def connecting(name, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # send user's name to the server
    s.send(name.encode("utf-8"))
    print("Server connected successfully")
    #threads are used to simultaneously run 'sendMessage', 'recieveMessage'
    g1 = threading.Thread(target=sendMessage, args=(s,))
    g1.start()
    g2 = threading.Thread(target=recieveMessage, args=(s,))
    g2.start()

#method to handle recieved messages
def recieveMessage(s):
    try:
        while True:
            data = s.recv(1024).decode("utf-8")
            #if this message was broadcasted by the server, this will print it without decrypting since it's not encrypted
            if (data[data.find(" ") + 1:] == "has joined the chat") or (data[data.find(" ") + 1:] == "has left the chat"):
                print(data)
            else:
                #this line stores received data until the symbol ":"
                #for example: n = "Anonymous:"
                n = data[0:(data.find(':')+1)]
                #this line stores received data from the next symbol to the end of the string
                #for example: n= "hello world"
                data_hash = data[(data.find('+')+1):len(data)]

                data = data[(data.find(':')+1):data.find('+')]

                data = getTranslatedMessage(data, -2)
                if data_hash == hashlib.md5(data.encode()).hexdigest():
                    print(n, data)
                else :
                    print ("the server is hacked")
                
                #decrypt recieved message
                
    #if server suddnly disconnects, this exception is thrown
    except ConnectionResetError:
        print("The server was unexpectedly disconnected")

#send message to server
def sendMessage(s):
    while True:
        message = str(input())
        message_hash = hashlib.md5(message.encode()).hexdigest()
        if  message == '':
            True
        #close conneciton if Client enters the string "exit" and end method
        elif message == "exit":
            s.send(message.encode("utf-8"))
            s.close()
            return
        #encrypt and send entered message
        else:
            x = (getTranslatedMessage(message, 2)+'+'+message_hash).encode("utf-8")
            s.send(x)



def getTranslatedMessage(message, key):
    translated = ''
    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key
            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            translated += chr(num)
        else:
            translated += symbol
    return translated

first(name, host, port)
