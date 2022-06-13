# multi-threaded app:  concurrently running
from socket import AF_NET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

#global constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZ = 512
MAX_CONNECTIONS = 10

#global variables
person = []
SERVER = socket(AF_NET, SOCK_STREAM)
SERVER.bind(ADDR) #set up server


def broadcast(msg, name):
    """
    send new messages to all clients
    param msg: bytes["utf8"]
    param name: str
    return: 
    """
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    """
    thread to handle all messages from client
    param person: Person
    return: none
    """
    client = person.client
    addr = person.addr

    # get person's name
    name = client.recv(BUFSIZ).decode()
    msg = f"{name} has joined the chat!"
    broadcast(msg) # broacast welcome message


    while True:
        try:
            msg = person.recv(BUFSIZ)
            print(f"{name}: ", msg.ecode("utf8"))


            if msg == bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat...", "")
                client.send(bytes("{quit}", "utf8"))
                client.close()
                person.remove(person)
                break
            else:
                broadcast(msg, name)
                
        except Exception as e:
            print("[EXCEPTION]", e)
            break      


# wait for any connection from client in an infinite loop
def wait_for_connection():
    """
    wait for connection from new clients, start new thread once connected to
    param server: Socket
    return: none
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, arg=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False    
    
    print("SERVER CRASHED")        


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #listen for connections
    print("waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


