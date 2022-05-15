import socketio

global socketClient
server_path = 'http://localhost:3000' # node server location
socket_connected = False

def connectSocket():
    try:
        socketClient = socketio.Client()
        socketClient.connect(server_path)
    except socketio.exceptions.ConnectionError as err:
        socket_connected = False
        print("Error on socket connection")
    else:
        socket_connected = True

def sendData (textSound):
    try:
        socketClient.emit('textSound', textSound)
    except socketio.exceptions.BadNamespaceError as err:
        print("error sending data", err)
