import socket

HOST = '192.168.68.109'
PORT = 1024
DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST'

def test_client():
    client = socket.socket()
    client.connect((HOST, PORT))
    while True:
        message = input('Please enter the key you would like to press: ')
        if message == 'done':
            client.send(DISCONNECT_MESSAGE.encode('utf-8'))
            client.close()
            return
        client.send(message.encode('utf-8'))

test_client()