"""A wordle game server created by Sam Selkregg"""
import socket
import threading
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


"""
    Function: handle_client
    Purpose: Turns client handling into a thread function to be able to handle multiple clients at once
    Returns: N/A
    Parameters: connection - the connection we have established to the client to send and recieve information
                clientAddress - the address of the client connected
"""
def handle_client(connection, clientAddress):
    print(f"Connected by: {clientAddress}")
    try:
        while True:
            ##display welcome message
            connection.sendall(
                b"HELLO! Welcome to WORDLE! Try to guess your word!\n"
                b"X - Incorrect Letter\n"
                b"Y - Correct Letter, Wrong Space\n"
                b"G - Correct Letter, Correct Space\n"
                b"XXXXX"
            )
            ##call select word function to select a random word for play
            word = wordleLibrary.select_word()

            while True:
                ##recieve guess
                guessData = connection.recv(1024)

                ##client disconnected or sent nothing
                if not guessData:
                    raise ConnectionError

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

            ##ask if they wanna play again (unless client bailed)
            playAgainMsg = connection.recv(1024)
            if not playAgainMsg:
                raise ConnectionError

            if playAgainMsg.decode().lower() == "n":
                break

    except ConnectionError:     ##something happened with the client connection (unexpected)
        print(f"Client {clientAddress} is gone buddy, sorry bout that G.")
    finally:        ##the game is over, we want to end the connection (expected)
        connection.close()
        print(f"The connection with {clientAddress} is no more. (But like on good terms.)")


try:
    while True:
        ##Accept a new client connection
        connection, clientAddress = serverSock.accept()
        ##Create a new thread so multiple clients can play at once
        clientThread = threading.Thread(target=handle_client, args=(connection, clientAddress))
        clientThread.daemon = True   ##so threads don't block shutdown
        clientThread.start()

except KeyboardInterrupt:   ##lets handle a keyboard server interrupt 
    print("\nWe gonna shut dis bad boy down.")

finally:    ##now we are done forreal forreal
    serverSock.close()
    print("Server ended successfully.")
