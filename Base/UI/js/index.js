var socket = io.connect('http://192.168.0.100:9000');

socket.on('onMessage', function (interceptedJSON) {
    if(interceptedJSON["UI"] == true){
        if("BotStatus" in interceptedJSON){
            $("#botStatus").val(interceptedJSON["BotStatus"])
        }
    }
});





//
//var connection = new autobahn.Connection({
//         url: 'ws://192.168.0.100:9000',
//         realm: 'realm1'
//      });
//
//connection.onopen = function (session) {
//
//    console.log("connected");
//};
//
//connection.open();