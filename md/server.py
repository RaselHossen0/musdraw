import socket
import threading
import random
import json

host = '127.0.0.1'
port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
draw_complete=[]
max_rounds = 4
current_round = 0
words = ['Elephant', 'Apple', 'Tree', 'Cow', 'Dog']
game_started = False

def broadcast(message, exclude=None):
    for client in clients:
        if client != exclude:
            try:
                client.send(json.dumps(message).encode('utf-8') + b'\n')  # Add newline as
            except:
                client.close()
                remove(client)

def remove(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast({'type': 'leave', 'message': f'{nickname} left the chat!'})
        print(f'{nickname} has disconnected.')

def handle(client):
    try:
        while True:
            message = json.loads(client.recv(1024).decode('utf-8'))
            if message.get('type') == 'message':
                broadcast(message, exclude=client)
            elif message.get('type') == 'draw':
                broadcast(message, exclude=client)
    except:
        remove(client)
def handle_round(current_round, clients, nicknames, words):
   print("Handling round")

   for i in range(len(clients)):
       
        drawer_nickname = nicknames[i]
        drawer_client = clients[i]

        broadcast({'type': 'message', 'message': f'Round {current_round}, {drawer_nickname} is drawing!'})
        broadcast({'type': 'word', 'word': words[i % len(words)]},exclude=drawer_client)
        drawer_client.send(json.dumps({'type': 'draw_start','nickname':f'{drawer_nickname}','message':f'{drawer_nickname} is drawing' ,'word': words[i % len(words)]}).encode('utf-8')+ b'\n')
        
        move_next = False
        while True:
            try:
                message = json.loads(drawer_client.recv(1024).decode('utf-8'))
                # print(message)
                if message.get('type') == 'draw':
                    broadcast(message, exclude=drawer_client)
                elif message.get('type') == 'drawing_end':
                    broadcast(message, exclude=drawer_client)
                    move_next = True
                    break
            except:
                remove(drawer_client)
                break
        if move_next:
            continue
        else:
           return True
   
       

def start_round():
    global current_round, clients

    if not clients:
        print("No clients connected, waiting for players...")
        broadcast({'type': 'message', 'message': 'Waiting for players...'})
        return

    current_round += 1

    if current_round > max_rounds:
        broadcast({'type': 'message', 'message': 'Game Over'})
        current_round = 0
        return

    one_round=handle_round(current_round, clients, nicknames, words)
    print("One round done")
    if one_round:
        start_round()
    else:
        broadcast({'type': 'message', 'message': 'Game Over'})
        current_round = 0
    
   
        

def start_game():
    global game_started

    if len(clients) >= 3 and not game_started:
        print("Starting game...")
        game_started = True
        start_round()

def receive():
    global clients, nicknames, game_started

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send(json.dumps({'type': 'request_nickname','message':'Give your name.'}).encode('utf-8')+b'\n')
        nickname = json.loads(client.recv(1024).decode('utf-8')).get('nickname')

        if nickname:
            nicknames.append(nickname)
            clients.append(client)
            print(f'Nickname of the client is {nickname}')
            broadcast({'type': 'message', 'message': f'{nickname} joined the chat!'})
            client.send(json.dumps({'type': 'message', 'message': 'Connected to the server!'}).encode('utf-8')+ b'\n')

            if len(clients) >= 3 and not game_started:
                start_game()

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.close()

def main():
    print("Server is listening...")
    receive()

if __name__ == '__main__':
    main()