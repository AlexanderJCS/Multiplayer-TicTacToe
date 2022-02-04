# Multiplayer-TicTacToe
A multiplayer tictactoe game using Python.

DIRECTIONS FOR HOSTING A GAME:
1. Open the "host.py" python file using an IDE. Under the IP constant, change the string to your local IP (under default gateway in ipconfig for Windows).
2. If you want people to connect outside of your local network, port forward port 1234 (or whatever port the constant is set to).
3. Finally run the python file (this was made using Python 3.8 so no guarantees it works with other versions). Hosting setup is done.

DIRECTIONS TO CONNECT TO A HOST:
1. When prompted to input an IP, input the host's IP address. If you are not connecting via LAN, they can find this IP by typing "what is my IP" in Google.
2. Input the port. This must match the PORT constant in the host's script. Default port is 1234.
3. That's it! Have fun playing TicTacToe.
