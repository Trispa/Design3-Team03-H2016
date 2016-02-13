var socket = require('socket.io');
var express = require('express');
var http = require('http');
var obj = require("../Shared/config.json");
var url=obj.url;
var port=obj.port;

var app = express();
app.use(express.static('../Client/UI'));

var server = http.createServer(app);
var io = socket.listen(server);

var allClients = [];
var botClientStatus = "Not connected";
var robot;

io.on('connection', function (client) {
    allClients.push(socket);
    io.emit('sendingBotClientStatus', botClientStatus);
    client.on('sendingBotClientStatus', function(status){
        console.log(status);
        robot = client;
        botClientStatus = status;
        io.emit('sendingBotClientStatus', status);
    });
    client.on('disconnect', function() {
        console.log('A client got disconnected');
        if(client == robot){
            console.log('Bad news, it\'s the bot');
            botClientStatus = "Not connected";
            io.emit('sendingBotClientStatus', botClientStatus);
        }
        var i = allClients.indexOf(client);
        allClients.splice(i, 1);
    });

    client.on('needUpdatedInfo', function(){
        io.emit('needUpdatedInfo');
    });
    client.on('sendingImage', function(encodedString){
        io.emit('sendingImage', encodedString);
    });
    client.on('sendingInfo', function(info){
        io.emit('sendingInfo', info);
    });

    client.on('needNewCoordinates', function(data){
        io.emit('needNewCoordinates', data);
    });
    client.on('sendingNextCoordinates', function(data){
        io.emit('sendingNextCoordinates', data);
    });

    client.on('sendingEndSignal', function(){
        io.emit('sendingEndSignal');
    });
});

server.listen(port, url);


