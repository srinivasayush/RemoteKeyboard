import socket
import time
import pydirectinput


DISCONNECT_MESSAGE = '!DISCONNECT-REQUEST|'
MOUSE_CLIENT_TYPE = '!MOUSE-CLIENT|'

def test_mouse_client():
    client = socket.socket()
    host = '0.tcp.ngrok.io'
    port = 15472
    port = int(port)
    client.connect((host, port))
    client.send(MOUSE_CLIENT_TYPE.encode('utf-8'))
    for _ in range(0, 20):
        mouse_coordinates = pydirectinput.position()
        parsed_coordinates = f'{mouse_coordinates[0]},{mouse_coordinates[1]}|'
        print(parsed_coordinates)
        client.send(parsed_coordinates.encode('utf-8'))
        time.sleep(1)

    client.send(DISCONNECT_MESSAGE.encode('utf-8'))
    client.shutdown(1)

test_mouse_client()
