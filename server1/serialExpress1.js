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
console.log('Simple static server listening at '+url+':'+port);


io.sockets.on('connection', function (socket) {
port.open(function(error) {

  if (error) {
    console.log('failed to open: ' + error);
  } else {
    // port.write("A");
    console.log('Serial open');
    port.on('data', function(data) {
    //console.log('data length: ' + data.length);
    console.log(data);
    //result = data.split(',')
    result = data;

    //recieve data from client to send to rfDuino
    socket.on('toLED', data)\
    
  
    // console.log(data);
    // console.log("You sent R=" + data.r + " G="+ data.g + " B="+ data.g);
    socket.emit('toScreen', { r: result, g: 0, b: 255- result });     
  



    
    // port.write("A");
    });


}
  
});
});