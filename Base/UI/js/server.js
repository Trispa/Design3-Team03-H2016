var socket = require('socket.io');
var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);

var io = socket.listen(server);

var url="10.248.96.8";
var port=9000;

var allClients = [];

var pythonClientStatus = "Not connected";
var robot;

io.on('connection', function (client) {
    allClients.push(socket);
    io.emit('pythonClientStatus', pythonClientStatus);
    client.on('pythonClientStatus', function(status){
        console.log(status);
        robot = client;
        pythonClientStatus = status;
        io.emit('pythonClientStatus', status);
    });
    client.on('disconnect', function() {
        console.log('A client got disconnected');
        if(client == robot){
            console.log('Bad news, it\'s the bot');
            pythonClientStatus = "Not connected";
            io.emit('pythonClientStatus', pythonClientStatus);
        }
        var i = allClients.indexOf(client);
        allClients.splice(i, 1);
    });
});

server.listen(port, url);


