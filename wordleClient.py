"""A command line WORDLE Game client created by Sam Selkregg"""
import socket

##Try Local Host, ACAD Didn't work
HOST = '127.0.0.1'

##The port number this program will bind to
PORT = 9097

##Create the socket for the client
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


##Connect to the server
clientSock.connect((HOST, PORT))

##Recieve Welcome Message
welcomeMsg = clientSock.recv(1024)
print(welcomeMsg.decode())

##GAME LOGIC
i = 0
while True:
    if i == 5:
        clientSock.sendall(b"f")
        print("Sorry you have failed, the correct word is: ")
        msg = clientSock.recv(1024)
        print(msg.decode().upper())
        break
    
    guess = input("Make your guess (Type 'q' to quit): ")

    if guess == "q":
        clientSock.sendall(b"q")
        break

    ##Make sure gues is of the correct length
    if len(guess)!=5:
        while len(guess)!=5:
            guess = input("Guess must be 5 characters, try again: ")
            if guess == "q":
                clientSock.sendall(b"q")
                break
    
    clientSock.sendall(guess.encode())

    result = clientSock.recv(1024)

    ##conver this to a string
    resultString = result.decode()

    if resultString == "GGGGG":
        print(f"{resultString}\nCONGRATULATIONS YOU WIN!!!")
        clientSock.sendall(b"w")
        break
    
    print(resultString)


    i += 1



clientSock.close()