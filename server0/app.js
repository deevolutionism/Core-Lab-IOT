//emit data to client
var bodyParser = require('body-parser');
var express = require("express");
var app = express();
var port = 8000;
var url='localhost'
var server = app.listen(port);
var io = require("socket.io").listen(server);
var serialport = require("serialport").SerialPort;
// var SerialPort = serialport.SerialPort;
// var sport = new SerialPort("/dev/ttyAMA0", {
// 	baudrate: 9600,
// 	parser: serialport.parsers.readline("\n")
// }, false);

var color1, color2, color3


app.use(express.static(__dirname + '/'));

var serialport = new SerialPort("/dev/ttyAMA0"); // replace this address with your port address
serialport.on('open', function(){
  // Now server is connected to Arduino
  console.log('Serial Port Opend');

  io.sockets.on('connection', function (socket) {
      //Connecting to client 
      console.log('Socket connected');
      

      serialport.on('data', function(data){
          	console.log(data);
			result = data.split(',')
			result[3]
				
			socket.emit('toScreen', {r: result[1], g: result[2],b: result[3]});
      });
  });
});





// app.use(express.static(__dirname + '/'));
// console.log('Simple static server listening at '+url+':'+port);
// io.sockets.on('connection', function (socket) {
// 	sport.open(function(error){
// 		if (error){
// 			console.log('failed to open: ' + error);
// 		} else {
// 			console.log('Serial open');
// 			sport.on('data', function(data){
// 				console.log(data);
// 				result = data.split(',')
// 				result[3]
				
// 				socket.emit('toScreen', {r: result[1], g: result[2],b: result[3]});
// 			});
// 		}

//   });
// }); //END OF SOCKET