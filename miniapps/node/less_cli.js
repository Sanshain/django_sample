const fs = require("fs");
var accord         = require('accord');
var assign         = require('object-assign');
var path           = require('path');
var replaceExt     = require('replace-ext');

const readlineSync = require('readline-sync');

var less           = accord.load('less');



/*

var exec = require('child_process').execFile;
var runCalc = function(){
   exec('calc.exe', function(err, data) {  
        console.log(err)
        console.log(data.toString());                       
    });  
}
runCalc();

*/






var options = {}

var _id = process.argv.indexOf("--src")+1;

if (_id) console.time('Time');

var opts = assign({}, {
	 compress: false,
	 paths: []
}, options);


var render = async function (str, opts){
	
	var file = {}
	
	try{
		res = await less.render(str, opts);
		
		file.contents = Buffer.from(res.result);
		file.path = replaceExt(opts.filename, '.css');


		fs.writeFileSync(file.path, file.contents)
		
		console.log('compilled successfull')
		
		console.timeEnd('Time');	
	}
	catch(err) {
		
		// Convert the keys so PluginError can read them
		err.lineNumber = err.line;
		err.fileName = err.filename;

		// Add a better error message
		err.message = err.message + ' in file ' + err.fileName + ' line no. ' + err.lineNumber;
		
		console.log(err.message)
	};//*/

}
	
var start = async function (){

	do{
		
		if (!_id){
			
			opts.filename = readlineSync.question('listening ');
			
			console.time('Time');
			
		}
		else opts.filename = process.argv[_id];


		if (!fs.existsSync(opts.filename)){
			
			console.log('file not found');
			
			break;		
			
		}

		var str = fs.readFileSync(opts.filename, "utf8");	
		
		console.log('file readed');
		
		await render(str, opts);
		
	} while(true);

	console.log('exit');

}

start();



