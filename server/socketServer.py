import socket
import threading
import pydirectinput
import pyautogui
from typing import Any


HOST = socket.gethostbyname(socket.gethostname())
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'
PINS = {
    '42': 'w',
    '40': 'a',
    '44': 'd',
    '43': 's',
    '41': 'ctrl',
    '45': 'shift',
    '31': 'e',
    '33': 'q',
    '35': 'space'
    
}

def log(log_title: str, log_message: str) -> None:
    print('[' + log_title.upper() + ']' + ': ' + log_message)

def handle_client(connection: socket, address: tuple):
    connected = True
    while connected:
        data = ''
        buffer = ''
        while buffer != '|':
            buffer: str = str(connection.recv(1).decode('utf-8'))
            data += buffer
        data = data.replace('|', '')
        log('DATA RECEIVED', f'{data} received from {address}')
        if data == DISCONNECT_MESSAGE:
            connected = False
        else:
            pin, state = data.split(',')
            state = str(state)
            pin = str(pin)
            if str(state) == '0':
                pydirectinput.keyDown(PINS[pin])
                log('KEYDOWN', f'keydown request for key {PINS[pin]} initiated...')
            elif str(state) == '1':
                pydirectinput.keyUp(PINS[pin])
                log('KEYUP', f'keyup request for pin {PINS[pin]} initiated...')

    connection.close()
    log('DISCONNECT', f'client from {address} disconnected. Terminating thread...')

def start_server() -> None:
    server = socket.socket()
    log('STARTING', 'server starting...')
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        log('INITIALIZED', f'Client initialized - connection from {addr}')
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

start_server()
