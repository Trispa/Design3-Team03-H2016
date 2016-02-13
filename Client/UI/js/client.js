var socket = io.connect();

socket.on("botClientStatus", function(msg){
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

socket.on("endSignal", function(){
    $("#buttonGo").prop("disabled",false);
});

setInterval(function(){ socket.emit("needUpdatedInfo");}, 5000);

function start(){
    socket.emit("needNewCoordinates");
    $("#buttonGo").prop("disabled",true);
}