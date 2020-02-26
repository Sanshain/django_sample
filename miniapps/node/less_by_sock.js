const fs = require("fs");
const sock = require('net');
const less = require('./_just_less')


var assign         = require('object-assign');

console.log('start listen for LESS by HAMLPY')

var options = {}


sock.createServer(function (socket) {
    console.log("connected");

    socket.on('data', async function(data) {
		 
console.time('Time');

		console.log('start render: ' + data.toString());

		var opts = assign({}, {
			 compress: false,
			 paths: [],
			 filename : data.toString()
		}, options);

		var str = fs.readFileSync(opts.filename, "utf8");		
		
		console.log(str.length + ' bytes')
		
		await less.render(str, opts)//*/

console.timeEnd('Time');

		socket.write('done');
			  
	});
	 
}).listen(9091, 'localhost');
//*/





























/*
var s = require('net').Socket();
s.connect(8080, 'localhost');
s.write('Hello');
s.end();
//*/