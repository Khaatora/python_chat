import socket
import threading

host = '127.0.0.1'
port = 50000
#Array to hold connected Clients' connection details
ips = []

#Array to hold connected Clients' names
names = []


def first(host, port):
    print ("Current host : ", host, "\n"
           "Current port : ", port, "\n\n"
           "Enter 1 to change host and port \n"
           "Enter 2 to connect \n"
           )
    #variable to check what the user wants to do
    control = str(input())
    if control == "1":
        changeHostPort()
    elif control == "2":
        startServer(host, port)
    else:
        print("Invalid input, try again")
        return first(host, port)


#Method to change the used host and port
def changeHostPort():
    host = str(input("Host : "))
    port = int(input("Port : "))
    first(host, port)


#method that starts the server and adds clients info in two array endpoints
def startServer(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Server is ready")
    s.listen()
    connect(s)

    
#this method continues running to accept connections and start 'recieveMessage' thread
def connect(s):
    while True:
        #variables that carries the client's info
        conn, addr = s.accept()
        #name of the sender
        name = conn.recv(1024).decode("utf-8")
        # append both the sender's name and IP
        names.append(name)
        ips.append(conn)
        print(name, "is connected")
        #broadcast the new client's name to all connected clients
        broadcast(conn, name, True)
        #Thread is used to simultaneously run 'recieveMessage' and 'connect'
        g1 = threading.Thread(target=recieveMessage, args=(conn, name,))
        g1.start()


#method to handle received messages from client and respond accroding to what they sent
def recieveMessage(conn, name):
    try:
        while True:
            #awaits Client to send message
            data = conn.recv(1024).decode("utf-8")
            #take action depending on recieved message
            if data == "exit":
                ips.remove(conn)
                names.remove(name)
                print(name, "has disconnected")
                conn.close()
                broadcast(conn, name, False)
                return
            else:
                #this message is encrypted
                sendMessage(conn, name, data)
                print (name,":",data)
    #if user suddenly disconnects from server, this exception will be thrown
    except ConnectionResetError:
        print(name+" has unexpectedly disconnected from the server")
        ips.remove(conn)
        names.remove(name)
        broadcast(conn, name, False)


#method to broadcast the name of the user that joined or left the chat
def broadcast(conn, name, connected):
    for connection in ips:
        if(connection!=conn and connected):
            connection.send((name+" has joined the chat").encode("utf-8"))
        elif(not connected):
            connection.send((name+" has left the chat").encode("utf-8"))


#Send Message to all Clients
def sendMessage(conn, name, data):
    x = name + ":" + data
    for connection in ips:
        if connection != conn:
            connection.send(''.join(list(x)).encode("utf-8"))
     
first(host, port)
