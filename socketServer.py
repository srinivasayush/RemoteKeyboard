import socket
import time
import threading
from typing import List, Tuple
import pydirectinput
import pynput

HOST = ''
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'
KEYBOARD_CLIENT_TYPE = '!KEYBOARD-CLIENT'
MOUSE_CLIENT_TYPE = '!MOUSE-CLIENT'
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

mouse = pynput.mouse.Controller()

def log(log_title: str, log_message: str) -> None:
    print(f'[{log_title.upper()}]: {str(log_message)}')

def removeAll(string: str, substrings: List[str]) -> str:
    '''Removes all occurences of a given list of substrings in a string'''
    for substring in substrings:
        string = string.replace(substring, '')
    return string

def move_mouse_smoothly(dx: int, dy: int, duration: float) -> None:
    duration = float(duration)
    if duration == 0:
        raise Exception(f"The duration parameter cannot be set to 0! Please provide a value greater than 0(in seconds)")
    steps: float = max(1.0, float(int(duration * 120.0)))
    for i in range(0, int(steps) + 1):
        mouse.move(dx/steps, dy/steps)
        time.sleep(float(duration/steps))

def receive_data_from_client(connection: socket.socket, address: tuple, final_character: str) -> str:
    data = ''
    buffer = ''
    while buffer != final_character:
        buffer: str = str(connection.recv(1).decode('utf-8'))
        data += buffer
    data = removeAll(data, ['\n', '\r', final_character])
    return data

def handle_keyboard_client(connection: socket.socket, address: tuple) -> None:
    while True:
        data = receive_data_from_client(connection, address, final_character='|')
        log('KEYBOARD DATA RECEIVED', f'{data} received from {address}')
        if data == DISCONNECT_MESSAGE:
            break
        else:
            pin, state = data.split(',')
            state = str(state)
            pin = str(pin)
            if str(state) == '0':
                pydirectinput.keyDown(PINS.get(pin))
                log('KEYDOWN', f'keydown request for key {PINS[pin]} initiated...')
            elif str(state) == '1':
                pydirectinput.keyUp(PINS.get(pin))
                log('KEYUP', f'keyup request for pin {PINS[pin]} initiated...')

    connection.close()
    log('KEYBOARD DISCONNECT', f'client from {address} disconnected. Terminating thread...')

def handle_mouse_client(connection: socket.socket, address: tuple) -> None:
    previous_coordinates: tuple = mouse.position
    while True:
        data = receive_data_from_client(connection, address, final_character='|')
        if data == DISCONNECT_MESSAGE:
            break
        else:
            new_x, new_y = data.split(',')
            current_coordinates = (int(new_x), int(new_y))
            dx = current_coordinates[0] - previous_coordinates[0]
            dy = current_coordinates[1] - previous_coordinates[1]
            dx /= 2
            dy /= 2
            move_mouse_smoothly(dx, dy, duration=0.2)
                

def handle_client(connection: socket.socket, address: tuple) -> None:
    '''Handles a socket client and checks whether the client is a keyboard or mouse client'''
    client_type = receive_data_from_client(connection, address, final_character='|')
    log('client type', client_type)
    if client_type == KEYBOARD_CLIENT_TYPE:
        handle_keyboard_client(connection, address)
    elif client_type == MOUSE_CLIENT_TYPE:
        handle_mouse_client(connection, address)

def start_server() -> None:
    server = socket.socket()
    log('STARTING', f'server starting on port {PORT}...')
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        log('INITIALIZED', f'Client initialized - connection from {addr}')
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        client_thread.join()

start_server()
