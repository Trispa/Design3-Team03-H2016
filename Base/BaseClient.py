from socketIO_client import SocketIO, LoggingNamespace

url="192.168.0.100"
port=9000

def receiveResponse(*args):
    print('receiveResponse', args)

with SocketIO(url, port, LoggingNamespace) as socketIO:
    socketIO.on('status', receiveResponse)
    socketIO.wait()