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
    io.emit('sendBotClientStatus', botClientStatus);
    client.on('sendBotClientStatus', function(status){
        console.log(status);
        robot = client;
        botClientStatus = status;
        io.emit('sendBotClientStatus', status);
    });
    client.on('disconnect', function() {
        console.log('A client got disconnected');
        if(client == robot){
            console.log('Bad news, it\'s the bot');
            botClientStatus = "Not connected";
            io.emit('sendBotClientStatus', botClientStatus);
        }
        var i = allClients.indexOf(client);
        allClients.splice(i, 1);
    });

    client.on('sendImage', function(encodedString){
        io.emit('sendImage', encodedString);
    });

    client.on('startSignal', function(){
        io.emit('startSignal');
    });

    client.on('startSignalRobot', function(data){
        io.emit('startSignalRobot', data);
    });

    client.on('needNewCoordinates', function(data){
        io.emit('needNewCoordinates', data);
    });
    client.on('sendNextCoordinates', function(data){
        io.emit('sendNextCoordinates', data);
    });

    client.on('sendEndSignal', function(){
        console.log("END");
        io.emit('sendEndSignal');
    });

    client.on('sendRefusingOrderSignal', function(){
        io.emit('sendRefusingOrderSignal');
    });
});

server.listen(port, url);


