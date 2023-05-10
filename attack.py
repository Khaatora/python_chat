import socket

host = '127.0.0.1'
port = 50000
name = "hacker"

def connecting(name, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # s.send(name.encode("utf-8"))
    print("Server connected successfully")
    recieveMessage(s)


def recieveMessage(s):
    try:
        while True:
            data = s.recv(1024).decode("utf-8")
            if (data[data.find(" ") + 1:] == "has joined the chat") or (data[data.find(" ") + 1:] == "has left the chat"):
                print(data)
            else:
                n = data[0:(data.find(':')+1)]
                data = data[(data.find(':')+1):len(data)]
                # attempts to decrypt the message and show all possible outcomes
                for x in range(26):
                    print(n, getTranslatedMessage(data, x))
    except ConnectionResetError:
        print("The server was unexpectedly disconnected")



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


connecting(name, host, port)
