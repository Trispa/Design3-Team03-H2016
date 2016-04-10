var socket = io.connect();

socket.on("sendBotClientStatus", function(msg){
    console.log(msg);
    $("#botStatus").text(msg);
});
socket.on("sendInfo", function(data){
    var image = new Image();
    console.log(data);
    $("#path").attr("src",'data:image/jpg;base64,' + data["encodedImage"]);
    $("#position").text(data["robotPosition"]);
    $("#orientation").text(data["robotOrientation"]);
});
socket.on('sendVoltage', function(data){
    $('#voltage').text(data);
});

socket.on("sendEndSignal", function() {
    $("#buttonGo").prop("disabled", false);
    stopTimer();
});

socket.on("sendManchesterInfo", function(manchesterInfo){
    $("#asciiCharacter").text(manchesterInfo["decryptedCharacter"]);
    if(manchesterInfo["target"]["forme"]){
        $("#target").text(manchesterInfo["target"]["forme"]);
    }
    else if(manchesterInfo["target"]["couleur"]){
            $("#target").text(manchesterInfo["target"]["couleur"]);

    }
});

socket.on("sendRefusingOrderSignal", function(){
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

function start(){
    socket.emit("startSignal");
    $("#buttonGo").prop("disabled",true);
    startTimer();
}

function sendManchesterCall(){
    socket.emit("readManchester")
}

function sendManchesterMockCall(){
    socket.emit("sendManchesterCode", "A")
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
    var isOver = false;
    if(seconds == 0){
        if(minutes == 0){
            stopTimer();
            socket.emit("sendEndSignal");
            $("#buttonGo").prop("disabled",true);
            isOver = true;
        }else{
            $("#minute-left").text(nextMinutes);
        }
        nextSeconds = 59;
    }
    if(!isOver){
        $("#seconds-left").text(nextSeconds);
    }


}

function stopTimer(){
    clearInterval(currentTimer);
}

function reset(){
    $("#buttonGo").prop("disabled",false);
    $("#seconds-left").text("0");
    $("#minute-left").text("10");
}

function startFromTreasure(){
    console.log("command launch");
    socket.emit("startFromTreasure");
}

function startFromTarget(){
    socket.emit("startFromTarget");
    sendManchesterMockCall();
}

//Debug section calls

function sendBotToChargingStation(){
    socket.emit("debugSendBotToChargingStation");
}
function alignBotToChargingStation(){
    socket.emit("debugAlignBotToChargingStation");
}
function searchAllTreasure(){
    socket.emit("debugSearchAllTreasure");
}
function sendBotToTreasure(){
    socket.emit("debugSendBotToTreasure");
}
function alignBotToTreasure(){
    socket.emit("debugAlignBotToTreasure");
}
function sendBotToTarget(){
    socket.emit("debugSendBotToTarget");
}
function alignBotToTarget(){
    socket.emit("debugAlignBotToTarget");
}
function initializeWorld(){
    socket.emit("initializeWorld");
}