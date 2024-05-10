import socket
import threading
import random

host = '127.0.0.1'
port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

max_rounds = 4
current_round = 0
words = ['Elephant', 'Apple', 'Tree', 'Cow', 'Dog']
game_started = False

def broadcast(message, exclude=None):
    for client in clients:
        if client != exclude:
            client.send(message)

def handle(client):
    global clients, nicknames
    try:
        while True:
            message = client.recv(1024)
            if message:
                broadcast(message)
    except:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f'{nickname} left the chat!'.encode('utf-8'))
        nicknames.remove(nickname)
        print(f'{nickname} has disconnected.')

def start_round():
    global current_round, clients
    if not clients:
        print("No clients connected, waiting for players...")
        return
    current_round += 1
    if current_round > max_rounds:
        broadcast('Game Over'.encode('utf-8'))
        current_round = 0
        return
    drawer_index = random.randint(0, len(clients) - 1)
    drawer_nickname = nicknames[drawer_index]
    broadcast(f'Round {current_round}, {drawer_nickname} is drawing!'.encode('utf-8'))
    broadcast(f'Word: {words[current_round - 1]}'.encode('utf-8'))
    clients[drawer_index].send('You are drawing now. Your word is: {}'.format(words[current_round - 1]).encode('utf-8'))
    broadcast('Draw'.encode('utf-8'), exclude=clients[drawer_index])

def start_game():
    global game_started
    if len(clients) >= 2 and not game_started:
        print("Starting game...")
        game_started = True
        start_round()

def receive():
    global clients, nicknames, game_started
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        if len(clients) >= 2 and not game_started:
            start_game()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def main():
    print("Server is listening...")
    receive()

if __name__ == '__main__':
    main()
