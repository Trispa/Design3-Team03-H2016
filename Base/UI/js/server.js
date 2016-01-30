var socket = require('socket.io');
var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);

var io = socket.listen(server);

var url="192.168.0.100";
var port=9000;

io.on('connection', function (client) {
    client.on('pythonClientStatus', function(status){
        console.log(status);
        io.emit('pythonClientStatus', status);
    });
});

server.listen(port, url);


