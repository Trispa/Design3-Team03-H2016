var socket = io.connect();

socket.on("sendingBotClientStatus", function(msg){
    console.log(msg);
    $("#botStatus").text(msg);
});
socket.on("sendingImage", function(encodedImage){
    var image = new Image();
    image.src = 'data:image/jpg;base64,' + encodedImage;
    $("#path").attr("src",'data:image/jpg;base64,' + encodedImage);
});

socket.on("sendingInfo", function(info){
    $("#asciiCharacter").text(info['decodedCharacter']);
    $("#target").text(info['target']);
    $("#voltage").text(info['voltage']);
});

socket.on("sendingEndSignal", function(){
    $("#buttonGo").prop("disabled",false);
});

setInterval(function(){ socket.emit("needUpdatedInfo");}, 3000);

function start(){
    socket.emit("needNewCoordinates");
    $("#buttonGo").prop("disabled",true);
}