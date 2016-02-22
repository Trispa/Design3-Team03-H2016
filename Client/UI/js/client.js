var socket = io.connect();

socket.on("sendBotClientStatus", function(msg){
    console.log(msg);
    $("#botStatus").text(msg);
});
socket.on("sendImage", function(encodedImage){
    var image = new Image();
    image.src = 'data:image/jpg;base64,' + encodedImage;
    $("#path").attr("src",'data:image/jpg;base64,' + encodedImage);
});

socket.on("sendInfo", function(info){
    $("#asciiCharacter").text(info['decodedCharacter']);
    $("#target").text(info['target']);
    $("#voltage").text(info['voltage']);
});

socket.on("sendEndSignal", function(){
    $("#buttonGo").prop("disabled",false);
});

setInterval(function(){ socket.emit("needUpdatedInfo");}, 3000);

function start(){
    socket.emit("needNewCoordinates");
    $("#buttonGo").prop("disabled",true);
}