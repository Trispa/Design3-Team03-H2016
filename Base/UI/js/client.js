var url = "http://192.168.0.100";
var port = 9000;

var socket = io.connect(url + ":" + port);

socket.on("pythonClientStatus", function(msg){
    console.log(msg);
    $("#botStatus").text(msg);
});