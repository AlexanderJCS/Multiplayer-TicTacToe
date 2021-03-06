import socket
import pickle
import time

wins = 0
losses = 0
ties = 0

opponent = "X"
you = "O'"
start_player = opponent
# The new round variable is not neccicarily if there is a new round, but if it is a new round and the client goes first.
new_round = False

HEADER_LENGTH = 64

IP = input("IP: ")
PORT = int(input("Port: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

print("Connected. Please wait for the opponent to make a move.")


def print_board(current_board):  # Prints the board.
    print("\n")
    for i in range(3):
        for x in range(3):
            if x != 2:
                print(current_board[i][x], end=" | ")
            else:
                print(current_board[i][x])

        if i != 2:
            print("----------")


def valid_move(x, y):  # Checks if the move is valid.
    return board[y][x] == " "


def reset_game():
    global wins, losses, start_player, new_round, ties
    print(win_check)

    if win_check == f"{you} wins!":
        wins += 1

    elif win_check == f"{opponent} wins!":
        losses += 1

    else:
        ties += 1

    print(f"Wins: {wins} Losses: {losses} Ties: {ties}")

    if losses > 0:
        print(f"W/L ratio: {wins / losses}")

    # Switch the starting player
    if start_player == you:
        new_round = False
        start_player = opponent

    else:
        new_round = True
        start_player = you

    time.sleep(2)


# Main game loop
while True:
    if not new_round:
        win_check = client_socket.recv(HEADER_LENGTH).decode("utf-8")

    # Check if the host won.
        if win_check != "no winner":
            reset_game()
            continue

    new_round = False

    # Recieve the board

    board = client_socket.recv(HEADER_LENGTH)
    board = pickle.loads(board)

    # Record the player's move
    while True:
        while True:
            try:
                print_board(board)
                move = input("Enter a move (x, y): ")
                move = move.split(",")
                move_x = int(move[0][0]) - 1
                move_y = int(move[1][-1]) - 1

                # Switchces the y positions so the bottom left is 1, 1 instead of 1, 3.
                if move_y == 0:
                    move_y = 2
                elif move_y == 2:
                    move_y = 0
                break

            except ValueError:
                print("Please input valid formatting: \"x, y\"")

            except IndexError:
                print("Please input valid formatting: \"x, y\"")

        if not valid_move(move_x, move_y):
            print("Invalid move.")
            continue

        move = [move_x, move_y]
        move = pickle.dumps(move)
        client_socket.send(move)
        break

    # Check if the client won
    win_check = client_socket.recv(HEADER_LENGTH).decode("utf-8")
    if win_check != "no winner":
        reset_game()

    print("Waiting for opponent...")
