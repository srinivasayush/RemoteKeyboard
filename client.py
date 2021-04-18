import socket
from pynput import keyboard


HOST = '127.0.0.1'
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'
KEYDOWN = '!KEYDOWN'
KEYUP = '!KEYUP'

def send(client_socket: socket.socket, message: str) -> None:
    message += '|'
    client_socket.send(message.encode('utf-8'))

client_socket = socket.socket()
client_socket.connect((HOST, PORT))

key_is_down = True

def on_press(key):
    global key_is_down
    if not key_is_down:
        key_is_down = True
        print('Pressed...')
        print(key)
        send(client_socket, f'{key},{KEYDOWN}')


def on_release(key):
    print('Released...')
    print(key)
    global key_is_down
    key_is_down = False
    send(client_socket, f'{key},{KEYUP}')
    if key == keyboard.Key.esc:
        # Stop listener
        key_is_down = False
        send(client_socket, DISCONNECT_MESSAGE)
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


client_socket.close()
