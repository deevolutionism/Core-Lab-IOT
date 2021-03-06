var bodyParser = require('body-parser');
var express = require("express");
var app = express();
var port = 8000;
var url='localhost'
var server = app.listen(port);
var io = require("socket.io").listen(server);
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;
var port1 = new SerialPort("/dev/ttyAMA0", {
	baudrate: 9600,
	parser: serialport.parsers.readline("\n")
}, false);


app.use(express.static(__dirname + '/'));
console.log('Simple static server listening at '+url+':'+port);


var serialData;

port1.open(function(error) {

  if (error) {
    console.log('failed to open: ' + error);
  } else {
  
    console.log('Serial open');
    port1.on('data', function(data) {
    //console.log('data length: ' + data.length);
    console.log(data);
    serialData = data;
    });


}
  
});


//socket.io stuff
io.sockets.on('connection', function (socket) {
  
    	console.log(serialData)
        result = serialData.split(',')
        result[3]

        socket.emit('toScreen', {r: result[1], g: result[2], b: result[3]});

  });