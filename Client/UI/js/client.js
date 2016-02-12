

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

socket.on("sendingVoltage", function(voltage){
    $("#voltage").text(voltage);
});

socket.on("endSignal", function(){
    $("#buttonGo").prop("disabled",false);
});

socket.on("needNewCoordinates", function(data){
    $("#asciiCharacter").text(data['decodedCharacter']);
    $("#target").text(data['target']);
});

setInterval(function(){ socket.emit("needUpdatedInfo");}, 5000);

function start(){
    socket.emit("needNewCoordinates");
    $("#buttonGo").prop("disabled",true);
}


//Affiche les images de la caméra dans le browser, solution temporaire qui sera
//éventuellement d'afficher les images traités par la vision via le socket
//window.addEventListener("DOMContentLoaded", function() {
//    var video = document.getElementById("video"),
//        videoObj = { "video": true },
//        errBack = function(error) {
//            console.log("Video capture error: ", error.code);
//        };
//
//    if(navigator.getUserMedia) {
//        navigator.getUserMedia(videoObj, function(stream) {
//            video.src = stream;
//            video.play();
//        }, errBack);
//    } else if(navigator.webkitGetUserMedia) {
//        navigator.webkitGetUserMedia(videoObj, function(stream){
//            video.src = window.webkitURL.createObjectURL(stream);
//            video.play();
//        }, errBack);
//    }
//    else if(navigator.mozGetUserMedia) {
//        navigator.mozGetUserMedia(videoObj, function(stream){
//            video.src = window.URL.createObjectURL(stream);
//            video.play();
//        }, errBack);
//    }
//}, false);