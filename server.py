import socket
import threading
from typing import List
import pydirectinput

HOST = ''
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'
KEYDOWN = '!KEYDOWN'
KEYUP = '!KEYUP'

def log(log_title: str, log_message: str) -> None:
    print(f'[{log_title.upper()}]: {str(log_message)}')

def removeAll(string: str, substrings: List[str]) -> str:
    '''Removes all occurences of a given list of substrings in a string'''
    for substring in substrings:
        string = string.replace(substring, '')
    return string

def receive_data_from_client(connection: socket.socket, final_character: str) -> str:
    data = ''
    buffer = ''
    while buffer != final_character:
        buffer: str = str(connection.recv(1).decode('utf-8'))
        data += buffer
    data = removeAll(data, ['\n', '\r', final_character])
    return data

def handle_keyboard_client(connection: socket.socket, address: tuple) -> None:
    while True:
        data = receive_data_from_client(connection, final_character='|')
        print(data)
        log('KEYBOARD DATA RECEIVED', f'{data} received from {address}')
        if data == DISCONNECT_MESSAGE:
            break
        else:
            key, action = [str(element) for element in data.split(',')]
            if action.upper() == KEYDOWN:
                log(KEYDOWN, f'keydown request for key {key} initiated...')
                pydirectinput.keyDown(key)
            elif action.upper() == KEYUP:
                log('KEYUP', f'keyup request for pin {key} initiated...')
                pydirectinput.keyUp(key)

    connection.close()
    log('KEYBOARD DISCONNECT', f'client from {address} disconnected. Terminating thread...')
        

def start_server() -> None:
    server = socket.socket()
    log('STARTING', f'server starting on port {PORT}...')
    server.bind((HOST, PORT))
    server.listen()

    while True:
        connection, address = server.accept()
        log('INITIALIZED', f'Client initialized - connection from {address}')
        client_thread = threading.Thread(target=handle_keyboard_client, args=(connection, address))
        client_thread.start()
        client_thread.join()

start_server()
