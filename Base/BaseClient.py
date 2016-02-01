from socketIO_client import SocketIO, LoggingNamespace

url="10.248.96.8"
port=9000

def receiveResponse(*args):
    print('receiveResponse', args)

with SocketIO(url, port, LoggingNamespace) as socketIO:
    socketIO.on('status', receiveResponse)
    socketIO.wait()