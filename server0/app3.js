var bodyParser = require('body-parser');
var express = require("express");
var app = express();
var port = 8000;
var url='localhost'
var server = app.listen(port);
var io = require("socket.io/socket.io.js").listen(server);
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;
var port = new SerialPort("/dev/ttyAMA0", {
  baudrate: 9600,
  parser: serialport.parsers.readline("\n")
}, false); 

var portdata;
app.use(express.static(__dirname + '/'));

io.sockets.on('connection', function (socket) {

socket.on('toSerial', function(data){
  console.log(data);
});

port.open(function(error) {

  if (error) {
    console.log('failed to open: ' + error);
  } else {
    // port.write("A");
    console.log('Serial open');
    port.on('data', function(data) {
    //console.log('data length: ' + data.length);
    console.log(data);
    result = data.split(',')
    result[3]

    // console.log(data);
    // console.log("You sent R=" + data.r + " G="+ data.g + " B="+ data.g);
    socket.emit('toScreen', { r: result[1], g: result[2], b: result[3] });     

    });


}
  
});
});
