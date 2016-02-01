from socketIO_client import SocketIO, LoggingNamespace

url="192.168.0.100"
port=9000

with SocketIO(url, port, LoggingNamespace) as socketIO:
    socketIO.emit('pythonClientStatus','Connected')
    socketIO.wait()