
const sock = require('net');

console.log('1')


sock.createServer(function (socket) {
    console.log("connected");

    socket.on('data', function (data) {
        console.log(data.toString());
		  
		  socket.write('Hello2');
    });
}).listen(9091, 'localhost');
//*/


/*
var s = require('net').Socket();
s.connect(8080, 'localhost');
s.write('Hello');
s.end();
//*/