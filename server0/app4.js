var bodyParser = require('body-parser');
var express = require("express");
var app = express();
var port = 8000;
var url='localhost'
var server = app.listen(port);
var io = require("socket.io").listen(server);
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;
var port = new SerialPort("/dev/ttyAMA0", {
  baudrate: 9600,
  parser: serialport.parsers.readline("\n")
}, false); 

app.use(express.static(__dirname + '/'));

port.open(function(error) {
io.socket.on('connection', function(socket){


  if (error) {
    console.log('failed to open: ' + error);
  } else {
  
    console.log('Serial open');
    port.on('data', function(data) {
    //console.log('data length: ' + data.length);
    console.log(data);
    
    });


}
  
});
});


io.sockets.on('connection', function (socket) {
	socket.on('toColor', function(data){
		console.log('recieved color data, now emiting toScreen.')
		socket.emit('toScreen', { r:data.r, g:data.g, b:data.b });
	});

});