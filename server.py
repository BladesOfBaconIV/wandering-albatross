
import socket

from dataclasses import dataclass
from game import Game, Piece
from utils import load_config, get_response, send_str


@dataclass
class Player:
    socket: socket.socket
    address: str
    username: str
    team: Piece


config = load_config()
SERVER_HOST = config["server-address"]
SERVER_PORT = config["server-port"]

server_socket = socket.create_server((SERVER_HOST, SERVER_PORT), backlog=0)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"Started server at {SERVER_HOST}:{SERVER_PORT} -- waiting for players")


def wait_for_player(team: Piece) -> Player:
    """
    Waits for a new player connection
    """
    player_socket, player_address = server_socket.accept()
    name = get_response(player_socket)
    print(f"[+] Player {name} {player_address} joined")
    return Player(socket=player_socket, address=player_address, username=name, team=team)


def start_players_turn(game: Game, player: Player) -> bool:
    """
    Handles the logic for a players turn, sending the current board, getting their move, and updating the board

    :return: bool, True if turn ended successfully, False if player disconnected
    """
    try:
        send_str(player.socket, str(game))  # Send the current board to the player
        send_str(player.socket, "Its your turn")
        while move := int(get_response(player.socket)):  # Get move, and ask again if move isn't valid
            if not game.is_move_valid(move):
                send_str(
                    player.socket, 
                    f"Move '{move}' is not valid for the current game, please enter a valid move"
                )
            else:
                break
        game.make_move(move, player.team)
        return True
    except Exception as e:  # TODO more specific Exception handling
        return False

def run():
    teams = [Piece.RED, Piece.YELLOW, ]  # teams for the game, first player is red, second is yellow
    players = []
    game = Game()
    turn = 0
    for team in teams:
        players.append(wait_for_player(team))
    while not (winner := game.is_won()) or not game.is_full():
        current_player = players[turn % 2]
        if not start_players_turn(game, current_player):
            send_str(players[(turn + 1) % 2].socket, f"Game over. Player {current_player.username} disconnected.")
            return
        turn += 1
        send_str(current_player.socket, f"Waiting for opponent to make a move")
    
    if winner is not Piece.EMPTY:   # If someone won the game
        winner_player = [p.username for p in players if p.team is winner].pop()
        end_message = f"{winner_player} won the game. Congratulations."
    else:  # Game was a draw due to no space left
        end_message = f"Looks like there's no space left, lets call it a draw"

    for player in players:
        send_str(player.socket, "--- GAME OVER ---")
        send_str(player.socket, f"{end_message}\n")
        player.socket.close()


if __name__ == "__main__":
    run()
    server_socket.close()