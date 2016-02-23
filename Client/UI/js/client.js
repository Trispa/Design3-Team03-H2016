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
    $("#position").text(info['position']);
    $("#orientation").text(info['orientation']);
});

socket.on("sendingRefusingOrderSignal", function(){
    if(!isTimerDone()){
        $("#buttonGo").prop("disabled",false);
        stopTimer();
    }
});

function isTimerDone(){
    var seconds = $("#seconds-left").text();
    var minutes = $("#minute-left").text();
    var returnedValue = false;
    if(seconds == 0) {
        if (minutes == 0) {
            returnedValue = true;
        }
    }
    return returnedValue;
}

setInterval(function(){ socket.emit("needUpdatedInfo");}, 3000);

function start(){
    socket.emit("startSignal");
    $("#buttonGo").prop("disabled",true);
    startTimer();
}

var currentTimer;

function startTimer(){
    currentTimer = setInterval(runTimer, 1000);
}

function runTimer(){
    var seconds = parseInt($("#seconds-left").text());
    var minutes = parseInt($("#minute-left").text());
    var nextSeconds = seconds - 1;
    var nextMinutes = minutes - 1;
    if(seconds == 0){
        if(minutes == 0){
            stopTimer();
            socket.emit("sendingEndSignal");
            $("#buttonGo").prop("disabled",true);
        }else{
            $("#minute-left").text(nextMinutes);
        }
        nextSeconds = 59;
    }else{
        $("#seconds-left").text(nextSeconds);
    }
}

function stopTimer(){
    clearInterval(currentTimer);
}

function reset(){
    $("#buttonGo").prop("disabled",false);
    $("#seconds-left").text("15");
    $("#minute-left").text("0");
}