import socket
from utils import load_config, get_response, send_str

config = load_config()
SERVER_HOST = config["server-address"]
SERVER_PORT = config["server-port"]

name = input("Enter your name: ")

server = socket.socket()
server.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected to game")
server.send(name.encode())

def listen_to_server():
    """
    Listens to the server and prints any messages recieved, 
    returning when its your turn or the game is over
    """
    while True:
        response = get_response(server)
        print(response)
        if "your turn" in response.lower() or "valid move" in response.lower():
            return True
        elif "game over" in response.lower():
            return False

while True:
    our_turn = listen_to_server()  # Listen to the server until the users turn starts
    if not our_turn:  # if stopped listenting but not our turn game has ended
        break
    while (to_send := input("Enter your move (1-9) or q to quit: ")).lower() != 'q':
        if to_send not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print("Please enter a number between 1 and 9 (inclusive), or q to quit")
        else:
            break
    else:
        break
    send_str(server, to_send)

server.close()