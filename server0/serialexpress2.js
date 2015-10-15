var bodyParser = require('body-parser');
var http = require('http');
var express = require('express');
var app = express();
var SerialPort = require("serialport").SerialPort;
var server = http.createServer(app).listen(3000);
var io = require('socket.io').listen(server);

app.use(express.static(__dirname + '/'));

var serialport = new SerialPort("/dev/ttyAMA0"); // replace this address with your port address
serialport.on('open', function(){
  // Now server is connected to Arduino
  console.log('Serial Port Opened');

  io.sockets.on('connection', function (socket) {
      //Connecting to client 
      console.log('Socket connected');
      

      serialport.on('data', function(data){
          console.log(data)
          result = data.split(',')
          result[3]

          socket.emit('toScreen', {r: result[1], g: result[2], b: result[3]});
      });
  });
});