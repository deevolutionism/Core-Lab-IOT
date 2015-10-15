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

//open the serial connection and begin reading
port1.open(function(error) {

  if (error) {
    console.log('failed to open: ' + error);
  } else {
  
    console.log('Serial open');
    port1.on('data', function(data) {
    //console.log('data length: ' + data.length);
    console.log('bit of data' + data);
    serialData = data;
    });


}
  
});


//socket.io stuff
io.sockets.on('connection', function (socket) {
  port1.open(function(error){
  	if(error){
  		console.log('failed to open: ' + error);
  	} else {
  		console.log('serial open within socket');
  		port1.on('data', function(data){
  			console.log(data)
  			console.log(serialData)
        	result = data.split(',')
       		result[3]
       		console.log('red: ' + result[1] + 'green: ' + result[2] + 'blue' + result[3]);
        	socket.emit('toScreen', {r: result[1], g: result[2], b: result[3]});
  		});
  	};
  });
  });