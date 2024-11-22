import socket
import threading

# Server Constants
SERVER_HOST = 'localhost'
SERVER_PORT = 5555
MAX_PLAYERS = 2

# Game Variables
board = [['' for _ in range(3)] for _ in range(3)]
players = []
turn = 'X'

# Functions
def handle_client(client_socket, player):
    global turn
    try:
        # Send welcome message to player
        client_socket.send(f"Player {player} connected. You are {player}".encode())

        while True:
            move = client_socket.recv(1024).decode()
            if move:
                row, col = map(int, move.split(','))
                if board[row][col] == '' and turn == player:
                    board[row][col] = player
                    turn = 'O' if player == 'X' else 'X'
                    # Send the updated board to both players
                    board_state = "\n".join([" | ".join(row) for row in board])
                    for p in players:
                        p.send(board_state.encode())
                else:
                    client_socket.send("Invalid move. Try again.".encode())
            else:
                break
    except Exception as e:
        print(f"Error with client {player}: {e}")
    finally:
        players.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(MAX_PLAYERS)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while len(players) < MAX_PLAYERS:
        client_socket, addr = server.accept()
        player = 'X' if len(players) == 0 else 'O'
        players.append(client_socket)
        print(f"Player {player} has joined the game.")
        threading.Thread(target=handle_client, args=(client_socket, player)).start()

if __name__ == "__main__":
    start_server()
