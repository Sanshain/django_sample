const fs = require("fs");

const performance = require('perf_hooks').performance;

var flname = "tst.txt"

var start;
var i = 0;
var aver = [];

fs.watchFile(flname, { interval: 10 }, (curr, prev) => {
	
	let perf = performance.now() - start;	
	
	console.timeEnd('watch');	
	
	console.log(perf)
	aver.push(perf);
	
	var sum = 0;
	for(var c = 0;c<aver.length;c++)sum+=aver[c];
	
	console.log('average: ' + sum/aver.length + ' by ' + aver.length)

	// console.log(`${flname} file Changed`);
	
	console.log('--------------------')
	
});

setInterval(function(){
	
	console.time('writeFileSync');

	fs.writeFileSync(flname, 'test - ' + ++i)

	console.timeEnd("writeFileSync");	
	
	
	start = performance.now()
	
	console.time('watch');	
		
	
}, 1500);




