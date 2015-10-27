var bodyParser = require('body-parser');
var express = require("express");
var app = express();
var port = 8000;
var url='localhost'
var server = app.listen(port);
var io = require("socket.io").listen(server);
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;
var sport = new SerialPort("/dev/tty.usbserial-DJ0081WH", {
  baudrate: 9600,
  parser: serialport.parsers.readline("\n")
}, false); 

app.use(express.static(__dirname + '/'));
console.log('Simple static server listening at '+url+':'+port);




io.sockets.on('connection', function (socket) {
sport.open(function(error) {

  if (error) {
    console.log('failed to open: ' + error);
  } else {

    console.log('Serial open');
    port.on('data', function(data) {

    console.log(data);  

    socket.emit('toScreen', data);     
  
    });

    socket.on('toRFduino', function(data){
      port.write(data);
      print("recieved data from client: " + data);
    });


}
  
});
});