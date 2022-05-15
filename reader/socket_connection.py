import socketio

global socketClient
server_path = 'http://localhost:3000' # node server location
is_connected = False

def connectSocket():
    try:
        socketClient = socketio.Client()
        socketClient.connect(server_path)
    except socketio.exceptions.ConnectionError as err:
        is_connected = False
        print("Error on socket connection")
    else:
        is_connected = True

def sendData (textSound):
    try:
        socketClient.emit('textSound', textSound)
    except socketio.exceptions.BadNamespaceError as err:
        print("error sending data", err)
