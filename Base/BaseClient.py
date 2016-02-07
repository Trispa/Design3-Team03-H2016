from socketIO_client import SocketIO, LoggingNamespace
import base64

url="192.168.0.100"
port=9000

def sendImage():
    encoded = base64.b64encode(open("UI/style/img/Picture 1.jpg", "rb").read())
    print(encoded)
    return encoded

with SocketIO(url, port, LoggingNamespace) as socketIO:
    socketIO.emit('sendingImage', sendImage())
    socketIO.wait()