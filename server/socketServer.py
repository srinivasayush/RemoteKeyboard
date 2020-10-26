import socket
import threading
from keypresser import press_key, release_key
from typing import Any


HOST = socket.gethostbyname(socket.gethostname())
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'
PINS = {
    '11': [0x11, False]
}


def press_key_in_background(pin: str) -> None:
    PINS[pin][1] = True

    def run() -> None:
        while PINS[pin][1] == True:
            press_key(PINS[pin][0])
        return

    press_thread = threading.Thread(target=run)
    press_thread.start()
    press_thread.join()

def release_key(pin: str) -> None:
    PINS[pin][1] = False


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
                press_key_in_background(pin)
                log('KEYDOWN', f'keydown request for key {PINS[pin][0]} initiated...')
            elif str(state) == '1':
                release_key(pin)
                log('KEYUP', f'keyup request for pin {PINS[pin][0]} initiated...')

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