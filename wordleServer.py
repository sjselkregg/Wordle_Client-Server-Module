"""A WORDLE Server Created by Sam Selkregg"""
import socket
import wordleLibrary

##Try local host, acad didn't work
HOST = '127.0.0.1'

##The port number this program will bind to
PORT = 9097

##Create the socket for the server
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##Allows for the port to be reused immediately after closing
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

##Bind the server socket to host and port so clients can connect
serverSock.bind((HOST, PORT))

serverSock.listen()
print(f"Server listening on Host:{HOST}, Port:{PORT} ")

try:
    while True:
        connection, clientAddress = serverSock.accept()

        print(f"Connected by: {clientAddress}")
        try:
            connection.sendall(b"HELLO! Welcome to WORDLE! Try to guess your word!\nX - Incorrect Letter\nY - Correct Letter, Wrong Space\nG - Correct Letter, Correct Space\nXXXXX")
            word = wordleLibrary.select_word()

            while True:
                guessData = connection.recv(1024)
                
                guess = guessData.decode()

                ##client has sent q to quit
                if guess == "q":
                    break

                ##client has won
                if guess == "w":
                    break

                ##client has failed, we will send the word and end
                if guess == "f":
                    connection.sendall(word.encode())
                    break

                ##call module function
                result = wordleLibrary.process_guess(word, guess)

                ##send our result to client
                connection.sendall(result.encode())
        except ConnectionError:     ##something happened with the client connection (unexpected)
            print(f"Client {clientAddress} is gone buddy, sorry bout that G.")
        finally:        ##the game is over, we want to end the connection (expected)
            connection.close()
            print(f"The connection with {clientAddress} is no more. (But like on good terms.)")
except KeyboardInterrupt:   ##lets handle a keyboard server interrupt 
    print("\nWe gonna shut dis bad boy down.")

finally:    ##now we are done forreal forreal
    serverSock.close()
    print("Server ended successfully.")
