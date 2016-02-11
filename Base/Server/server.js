var socket = require('socket.io');
var express = require('express');
var http = require('http');
var obj = require("../../Shared/config.json");

var app = express();
app.use(express.static('Client/UI'));

var server = http.createServer(app);
var io = socket.listen(server);

var url=obj.url;
var port=obj.port;

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

    client.on('needNewImage', function(){
       io.emit('needNewImage');
    });
    client.on('sendingImage', function(encodedString){
        io.emit('sendingImage', encodedString);
    });

    client.on('launch', function(){
        io.emit('launch');
    });
    client.on('goBot', function(data){
        io.emit('goBot', data);
    });

    client.on('needTreasurePath', function(){
        io.emit('needTreasurePath');
    });
    client.on('sendingTreasurePath', function(data){
        io.emit('sendingTreasurePath', data);
    });

    client.on('needTargetPath', function(){
        io.emit('needTargetPath');
    });
    client.on('sendingTargetPath', function(data){
        io.emit('sendingTargetPath', data);
    });

    client.on('endSignal', function(){
        io.emit('endSignal');
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


