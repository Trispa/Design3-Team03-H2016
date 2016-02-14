$.getJSON('../../Shared/config.json', function(json) {
    var url = "http://" + json.url;
    var port = parseInt(json.port);

    var socket = io.connect(url + ":" + port);

    socket.on("pythonClientStatus", function(msg){
        console.log(msg);
        $("#botStatus").text(msg);
    });
    socket.on("sendingImage", function(encodedImage){

        var image = new Image();
        image.src = 'data:image/jpg;base64,' + encodedImage;
        $("#path").attr("src",'data:image/jpg;base64,' + encodedImage);

    });
    function start(){
        socket.emit("launch");
    }
});



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