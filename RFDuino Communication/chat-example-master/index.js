var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;
var sport = new SerialPort("/dev/cu.usbserial-DJ0081WH", {
  baudrate: 9600,
  parser: serialport.parsers.readline("\n")
}, false); 

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
	sport.open(function(error) {
		if(error){
			console.log('failed to open: ' + error);
		} else {
			consol.log('serial open');
			sport.on('data', function(data){
				console.log(data);
				io.emit('chat message', data);
			});
		}
	});
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
