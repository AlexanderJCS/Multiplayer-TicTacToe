import socket
import time
import threading
import pickle

wins = 0
losses = 0
ties = 0

you = "X"
opponent = "O"
turn = opponent
start_player = you

board = [[" " for _ in range(3)] for _ in range(3)]
moves = 0

HEADERSIZE = 64

IP = socket.gethostbyname(socket.gethostname())
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen(2)

clients = []


def manage_clients():  # Candle clients connecting and disconnecting
    clientsocket, address = server_socket.accept()

    # Accepts only 1 client
    if len(clients) > 1:
        clientsocket.close()

    else:
        clients.append(clientsocket)


def print_board(current_board):
    for i in range(3):
        for x in range(3):
            if x != 2:
                print(current_board[i][x], end=" | ")
            else:
                print(current_board[i][x])

        if i != 2:
            print("----------")


def win_check():
    # Check columns
    if board[0][0] == board[0][1] == board[0][2] != " ":
        return f"{board[0][0]} wins!"

    if board[1][0] == board[1][1] == board[1][2] != " ":
        return f"{board[1][0]} wins!"

    if board[2][0] == board[2][1] == board[2][2] != " ":
        return f"{board[2][0]} wins!"

    # Check rows

    if board[0][0] == board[1][0] == board[2][0] != " ":
        return f"{board[0][0]} wins!"

    if board[0][1] == board[1][1] == board[2][1] != " ":
        return f"{board[0][1]} wins!"

    if board[0][1] == board[1][1] == board[2][1] != " ":
        return f"{board[0][2]} wins!"

    # Check diagonals

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return f"{board[0][0]} wins!"

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return f"{board[0][0]} wins!"

    # Check tie

    if moves >= 9:
        return "Tie"

    return "no winner"


def valid_move(x, y):
    return board[y][x] == " "


def restart_game():  # Restart the round and switch which player goes first
    global start_player, turn, board, moves, wins, losses, ties
    won = win_check()
    print_board(board)
    print(f"{won}\n")

    if won == f"{you} wins!":
        wins += 1

    elif won == f"{opponent} wins!":
        losses += 1

    else:
        ties += 1

    print(f"Wins: {wins} Losses: {losses} Ties {ties}")

    if losses > 0:
        print(f"W/L ratio: {wins / losses}")

    if start_player == you:
        turn = you
        start_player = opponent

    else:
        turn = opponent
        start_player = you

    board = [[" " for _ in range(3)] for _ in range(3)]
    moves = 0
    time.sleep(2)


# Main game
if __name__ == "__main__":

    t = threading.Thread(target=manage_clients)
    t.start()

    print("Waiting for player to connect...")

    # Wait for player
    while len(clients) < 1:
        time.sleep(1)

    client_socket = clients[0]

    print("Opponent connected.")

    while True:
        # If it is the host's turn, record the host's move.
        if turn == opponent:
            turn = you

            while True:
                while True:
                    try:
                        print_board(board)
                        move = input("Enter a move (x, y): ")
                        move = move.split(",")
                        move_x = int(move[0][0]) - 1
                        move_y = int(move[1][-1]) - 1

                        # Switchces the y coordinates so the bottom is y = 1 instead of y = 3.
                        if move_y == 0:
                            move_y = 2
                        elif move_y == 2:
                            move_y = 0
                        break

                    except ValueError:
                        print("Please input valid formatting: \"x, y\"")

                    except IndexError:
                        print("Please input valid formatting: \"x, y\"")

                # Check if the move is valid
                if valid_move(move_x, move_y):
                    board[move_y][move_x] = turn
                    moves += 1
                    break

                # If move is invalid, ask for a different move.
                else:
                    print("Invalid move.")
                    continue

            # Send to the client if the host won
            client_socket.send(win_check().encode("utf-8"))
            if win_check() != "no winner":
                restart_game()

        # If it is the client's move
        else:
            turn = opponent
            # Send board information to the client and wait for a response
            msg = pickle.dumps(board)
            client_socket.send(msg)
            print("Waiting for opponent...")

            opponent_moves = client_socket.recv(HEADERSIZE)

            moves += 1

            # Decode move information sent by the client.
            opponent_moves = pickle.loads(opponent_moves)
            opponent_move_x = opponent_moves[0]
            opponent_move_y = opponent_moves[1]

            if valid_move(opponent_move_x, opponent_move_y):
                board[opponent_move_y][opponent_move_x] = turn

            # Send to the client if they won.

            client_socket.send(win_check().encode("utf-8"))
            if win_check() != "no winner":
                restart_game()
